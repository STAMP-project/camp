---
layout: default
---

# The OW2/Lutece Use-case

This case-study illustrates how CAMP can build multiple variations
from a single docker-compose orchestration.


---
**Note**.
This case study is under development and is very likely to change.

---

This case-study focuses on deploying the
[Lutece](http://www.lutece.paris.fr/) content management
system. Lutece is common JEE application, that runs on a servlet
container such as [Tomcat](http://www.lutece.paris.fr/) and let users
develop their own CMS systems. In this case study, Lutece use
[MySQL](https://www.mysql.com/) to store all content.


<a name="inputs"/>
## The Required Inputs

The sample directory contains two main entities:

 1. the `camp.yml` file that defines what can vary in the X-Wiki
	orchestration.

 2. the `template` directory, which contains a template implementation
	of the orchestrations using Docker (and docker-compose).


### The CAMP Model

The CAMP model (i.e., the `camp.yml` file) defines what can be varied
in the orchestration. In this use-case, we focus on having multiple
versions/configuration of the same components.


```yaml
goals:
  running:
   - Lutece

components:

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
		type: version
		values: [ 5_6, 5_7 ]
		realization:
		  - targets: [ mysql/Dockerfile ]
			pattern: "FROM mysql:5"
			replacements: [ "FROM mysql:5.6", "FROM mysql:5.7" ]
	implementation:
	  docker:
		file: mysql/Dockerfile
```

The objective (i.e., the `goal`) is to get the Lutece application up
and running.

Here we define two components, namely `lutece`, the application
server, and `mysql`, the database where data are stored. Note that
both component are implemented using a dedicated Dockerfile.


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

├── docker-compose.yml
├── lutece
│   ├── Dockerfile
│   └── site-edito-mini.war
└── mysql
	├── Dockerfile
	└── sql-scripts
		└── site-edito-mini.sql
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

![Lutece Configuration]({{site.baseurl}}/assets/images/lutece_configurations.png
"The configurations that CAMPS generate to cover the OW2/Lutece case")

To better visualize these configurations, we can generate such an
image using Graphviz and Image Magic as follows. The figure below
illustrates these selected configurations.

```console
$ find . -name "*.dot" | xargs -I file dot -Tpng file -o file.png
$ find . -name "*.png" \
   | tr '\n' ' ' \
   | montage  -label '%d/%f' @- -geometry 300x300 configurations.png

```


<a name="coverage"/>
## How to Cover All Single Variations?

The command to search of a subset of configurations that covers all
single variations is:

```console
$ camp generate -d . --coverage
```

In this simple case, the two previous configurations are needed to
cover single variations.


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
├── config_1
│   ├── configuration.dot
│   ├── configuration.yml
│   ├── docker-compose.yml
│   └── images
│       ├── build_images.sh
│       ├── lutece_0
│       │   ├── Dockerfile
│       │   └── site-edito-mini.war
│       └── mysql_0
│           ├── Dockerfile
│           └── sql-scripts
│               └── site-edito-mini.sql
└── config_2
	├── configuration.dot
	├── configuration.yml
	├── docker-compose.yml
	└── images
		├── build_images.sh
		├── lutece_0
		│   ├── Dockerfile
		│   └── site-edito-mini.war
		└── mysql_0
			├── Dockerfile
			└── sql-scripts
				└── site-edito-mini.sql
```

To run these configurations, we must first build the related docker
images. CAMP generates a shell script (`out/images/build_images.sh`)
to facilitate just that. We simply run:

```
$ cd out/config_1/images
$ source ./build_images.sh
```

Once the images are built, we can now start our orchestration using
docker-compose as follows:

```
$ cd out/config_1
$ docker-compose -f docker-compose.yml up
```
