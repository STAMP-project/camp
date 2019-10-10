---
layout: default
---

# The OW2/Lutece Use-case

This case-study illustrates how CAMP can to run JMeter performance
tests against multiple versions of the environment.


This case-study focuses on deploying the
[Lutece](http://www.lutece.paris.fr/) content management
system. Lutece is common JEE application, that runs on a servlet
container such as [Tomcat](http://tomcat.apache.org/) and let users
develop their own CMS systems. In this case study, Lutece use
[MySQL](https://www.mysql.com/) to store all content.


<a name="inputs"/>
## The Required Inputs

The sample directory contains two main entities:

 1. the `camp.yml` file that defines what can vary in the OW2/Lutece
	orchestration.

 2. the `template` directory, which contains a template implementation
	of the orchestrations using Docker (and docker-compose).


### The CAMP Model

The CAMP model (i.e., the `camp.yml` file) defines what can be varied
in the orchestration. In this use-case, we focus on having multiple
versions/configuration of the same components. We have identified
three components, tests, lutece and storage. The `tests` component
represents the node where the performance testing tool (JMeter) is
deployed. The `lutece` component represents the Java web-app under
test whereas the `storage` component represents the storage solution
(MySQL).


```yaml
goals:
  running:
    - PerfTests

components:

  tests:
    provides_services: [ PerfTests ]
    requires_services: [ Lutece ]
    implementation:
      docker:
        file: tests/Dockerfile
    tests:
      command: -n -t Forms-test.jmx -l Forms-test.jtl -e -o results
      reports:
        format: jmeter
        location: results
        pattern: statistics.json

  lutece:
    provides_services: [Lutece]
    requires_services: [MySQL]
    implementation:
      docker:
        file: lutece/Dockerfile

  mysql:
    provides_services: [MySQL]
    variables:
      version:
          values: [ 5_6, 5_7 ]
          realization:
            - targets: [ mysql/Dockerfile ]
              pattern: "FROM mysql:5"
              replacements: [ "FROM mysql:5.6", "FROM mysql:5.7" ]
    implementation:
      docker:
        file: mysql/Dockerfile
```

The objective (i.e., the `goal`) is to get the performance tests up
and running. This implies that the Lutece application is also up and
running and, in turn, that the storage is ready too.

Here we define two components, namely `lutece`, the application
server, and `mysql`, the database where data are stored. All
components are implemented using a dedicated Dockerfile.


### The Template

In order to build configuration that we can run, CAMP needs a template
implementation of the orchestrations. This template must include:

 1. A docker-compose file, which illustrates the bindings and the
	configuration of each service.

 2. Dockerfile (and any other configurations) files for the services
	whose image must be built from scratch.

In this case, the template directory specifies the implementation of
both the `lutece` and `mysql` component.


```console
$ tree template
template
├── docker-compose.yml
├── lutece
│   ├── db.properties
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── pom.xml
├── mysql
│   ├── Dockerfile
│   └── sql-scripts
└── tests
    ├── Dockerfile
    ├── Forms-test.jmx
    ├── Forms-test.jtl
    └── jmeter.log
```

The `docker-compose.yml` file simply defines how to deploy and connect
`lutece` and `mysql`.

The `lutece` Dockerfile install the `site-demo-mini` web application
in a Tomcat 8, running on top of a Java runtime environment (JRE) 8.

The `mysql` Dockerfile uses the `site-demo-mini.sql` to initialize the
database using MySQL 5.

You can run the mysql container locally using the following commands:
```console
$ docker run -p 3306:3306 --name ow2-mysql -e MYSQL_ROOT_PASSWORD=whatever -d ow2/mysql
$ docker exec -it ow2-mysql bash
$ mysql -uroot -p
mysql> show databases;
...
```

<a name="generate-all"/>
## How to Generate All Configurations?

As for other case-studies, you can generate all possible
configurations with the following command:

```console
$ camp generate -d . --all
```

In this simple example, there are only two configurations, which are
shown below:

![Lutece Configuration]({{site.baseurl}}/assets/images/lutece_all_configs.png
"The configurations that CAMPS generate to cover the OW2/Lutece case")

To better visualise these configurations, we can generate such an
image using Graphviz and Image Magic as follows. The figure below
illustrates these selected configurations.

```console
$ find . -name "*.dot" | xargs -I file dot -Tpng file -o file.png
$ find . -name "*.png" \
   | tr '\n' ' ' \
   | montage  -label '%d/%f' @- -geometry 500x500 configurations.png

```

<a name="realize"/>
## How to Realize the Configurations?

CAMP has generated configuration in the `out` directory. But so far,
CAMP only generates a YAML file for each configuration that indicates
how components are wired and their configurations.

To transform those into real Docker configurations that we can run, we
invoke the following command:

```console
$ camp realize -d .
CAMP v0.1.0 (MIT)
Copyright (C) 2017, 2018 SINTEF Digital

Model loaded from './camp.yml'.
Searching configurations in './out' ...
 - Building './out/config_1' ...
 - Building './out/config_2' ...

That's all folks!
```

We can see that CAMP has generate modified the template for each
configurations. For instance:

```console
$ tree out
out
├── config_2
│   ├── configuration.dot
│   ├── configuration.yml
│   ├── docker-compose.yml
│   ├── images
│   │   ├── build_images.sh
│   │   ├── lutece_0
│   │   │   ├── db.properties
│   │   │   ├── Dockerfile
│   │   │   ├── entrypoint.sh
│   │   │   └── pom.xml
│   │   ├── mysql_0
│   │   │   ├── Dockerfile
│   │   │   └── sql-scripts
│   │   │       └── dump.sql
│   │   └── tests_0
│   │       ├── Dockerfile
│   │       ├── Forms-test.jmx
│   │       ├── Forms-test.jtl
│   │       └── jmeter.log
```

Looking at the Dockerfile of Configuration 2, we can see that CAMP did
carry out replacement to force the usage of MySQL 5.7, instead of
MySQL 5.6 in Configuration 1.

```dockerfile
FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD motdepasse
ENV MYSQL_DATABASE lutece

COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
```


## How to Test the Configurations?

At this stage, the configuration are ready to be executed. To runs the
tests in all configurations, simply invoke `camp execute` as follows:

```console
$ camp execute -d .
CAMP v0.6.3 (MIT)
Copyright (C) 2017 -- 2019 SINTEF Digital

Loaded './camp.yml'.
Loading configurations from './out' ...

 - Executing ./out/config_1
   1. Building images ...
      $ bash build_images.sh (from './out/config_1/images')
   2. Starting Services ...
      $ docker-compose up -d (from './out/config_1')
   3. Running tests ...
      $ docker-compose run tests -n -t Forms-test.jmx -l Forms-test.jtl -e -o results (from './out/config_1')
   4. Collecting reports ...
      $ docker ps --all --quiet --filter name=config_1_tests_run_ (from './out/config_1')
      $ docker cp 708b84623ff9:/tests/results ./test-reports (from './out/config_1')
      Reading statistics.json
   5. Stopping Services ...
      $ docker-compose down --volumes --rmi all (from './out/config_1')

 - Executing ./out/config_2
   1. Building images ...
      $ bash build_images.sh (from './out/config_2/images')
   2. Starting Services ...
      $ docker-compose up -d (from './out/config_2')
   3. Running tests ...
      $ docker-compose run tests -n -t Forms-test.jmx -l Forms-test.jtl -e -o results (from './out/config_2')
   4. Collecting reports ...
      $ docker ps --all --quiet --filter name=config_2_tests_run_ (from './out/config_2')
      $ docker cp 22d4d293e73f:/tests/results ./test-reports (from './out/config_2')
      Reading statistics.json
   5. Stopping Services ...
      $ docker-compose down --volumes --rmi all (from './out/config_2')

Test SUMMARY:

Configuration                 RUN   PASS   FAIL  ERROR
-------------------------------------------------------
./out/config_1                136    136      0      0
./out/config_2                116    106      1      9
-------------------------------------------------------
TOTAL                         252    242      1      9

That's all folks!
```

We see that that 136 tests pass against the first configuration. By
contrast, 116 tests were run against Configuration 2, 1 test failed
and 9 raised errors.
