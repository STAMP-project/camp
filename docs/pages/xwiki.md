---
layout: default
---

# The X-Wiki Use-case

The X-Wiki case-study illustrates how to vary the wiring between both
the services of the orchestrations, but also between component of a
single software stack (i.e., within a single container). In
particular, we details how to:

 1. [Generate all possible configurations](#general-all);
 2. Generate enough configurations to [cover all single variations](#coverage)
 3. Realize and [run the generated configurations](#realize)

The X-Wiki application is a Java service running on top of Tomcat, in
turn running on top of a Java Runtime Environment (JRE). X-Wiki uses a
database to persist its data, either MySQL or Postgres. By contrast,
with the [CityGo case-study](citygo.html), there is no numerical
variable involved.

The inputs files are located in the GitHub repository under
`samples/stamp/xwiki`. You may fetch them as follows:

```console
$ git clone https://github.com/STAMP-project/camp
$ cd camp/samples/stamp/xwiki
```

We assume hereafter that you already have CAMP up and running. If not,
please refer to the [installation instructions](setup.html).


<a name="inputs"/>
## The Required Inputs

The sample directory contains two main entities:

 1. the `camp.yml` file that defines what can vary in the X-Wiki
	orchestration.

 2. the `template` directory, which contains a template implementation
	of the orchestrations using Docker (and docker-compose).

### The CAMP Model

The CAMP model (i.e., the `camp.yml` file) defines what can be varied
in the orchestration. In this use-case, we focus on alternative
services providers and alternative component versions.

Here, our objective is to get the XWiki **service** up and running.

```yaml
goals:
  running:
	- XWiki

[...]
```

For instance, we define two version of MySQL, one for Version 5 and
one for Version 8. Both provide the `MySQL` **service**, which is
required by some of the X-Wiki components.

```yaml
components:
  [...]

  xwiki9mysql:
	provides_services: [XWiki]
	requires_services: [MySQL]
	requires_features : [Tomcat]
	implementation:
	  docker:
		file: xwiki9mysql/Dockerfile

  [...]

  mysql5:
	provides_services: [MySQL]
	implementation:
	  docker:
		image: mysql:5

  mysql8:
	provides_services: [MySQL]
	implementation:
	  docker:
		image: mysql:8
```

We proceed similarly for varying the underlying component that forms a
container. For instance, we define two versions of the JRE, namely
`openjdk8` and `openjdk9`. They both provide a **feature** that Tomcat
components require.

```yaml
components:
 [...]

  openjdk8:
	provides_features: [JRE]
	implementation:
	  docker:
		image: openjdk:8

  openjdk9:
	provides_features: [JRE]
	implementation:
	  docker:
		image: openjdk:9
```

### The Template

In order to build configuration that we can run, CAMP needs a template
implementation of the orchestrations. This template must include:

 1. A docker-compose file, which illustrates the bindings and the
	configuration of each service.

 2. Dockerfile (and any other configurations) files for the services
	whose image must be built from scratch.

In the X-Wiki case, the template directory specifies an implementation
of every components whose image is not to be downloaded directly from
the Docker hub.


```console
$ tree template
├── docker-compose.yml
├── tomcat7
│   └── Dockerfile
├── tomcat8
│   └── Dockerfile
├── tomcat85
│   └── Dockerfile
├── tomcat9
│   └── Dockerfile
├── xwiki8mysql
│   ├── Dockerfile
│   ├── mysql
│   │   └── xwiki.cnf
│   ├── tomcat
│   │   └── setenv.sh
│   └── xwiki
│       ├── docker-entrypoint.sh
│       └── hibernate.cfg.xml
├── [...]
```

Note the `docker-compose.yml` at in the top-level folder, as well as
the configuration file given for MySQL, X-Wiki and Tomcat in the
`xwiki8mysql` sub-directory.

<a name="generate-all"/>
## How to Generate All Configurations?

As for other case-studies, you can generate all possible
configurations with the following command:

```console
$ camp generate -d . --all
```

For X-Wiki, **there are exactly 64 possible configurations** and the
generation may take **about 50 minutes**, depending on how fast is your
machine.

These 64 configurations are basically all the permutations of
databases (MySQL or Postgres and their possible versions), application
server (Tomcat), JRE (openjdk) and XWiki.

CAMP generates a directory named `out` that contains a sub-directory
for each configuration generated.


<a name="coverage"/>
## How to Cover All Single Variations?

The command to search of a subset of configurations that covers all
single variations is:

```console
$ camp generate -d . --coverage
CAMP v0.1.0 (MIT)
Copyright (C) 2017, 2018 SINTEF Digital

Model loaded from './model.yml'.
Searching for configurations ...

 - Config. 1 in './out/config_1/configuration.yml'.
   Includes xwiki8postgres, postgres9, tomcat8, openjdk8

 - Config. 2 in './out/config_2/configuration.yml'.
   Includes postgres10, tomcat7, xwiki9postgres, openjdk9

 - Config. 3 in './out/config_3/configuration.yml'.
   Includes openjdk8, mysql5, tomcat9, xwiki8mysql

 - Config. 4 in './out/config_4/configuration.yml'.
   Includes mysql8, xwiki9mysql, tomcat85, openjdk9

That's all folks!
```

CAMP finds **a subset of 4 configurations that covers all single
variations**, that is all versions&mdash;listed in the CAMP
model&mdash;of all databases, JRE and applications servers are used at
least once.

The figure below illustrates these configurations.

![X-Wiki coverage]({{site.baseurl}}/assets/images/xwiki_coverage.png
"The configurations that CAMPS generate to cover the X-Wiki case")

To better visualize these configurations, we can generate such an
image using Graphviz and Image Magic as follows. The figure below
illustrates these selected configurations.

```console
$ find . -name "*.dot" | xargs -I file dot -Tpng file -o file.png
$ find . -name "*.png" \
   | tr '\n' ' ' \
   | montage  -label '%d/%f' @- -geometry 300x300 configurations.png

```

<a name="realize"/>
## How to Realize the Configurations?

CAMP has generated configuration in the `out`. But so far, CAMP only
generates a YAML file for each configuration that indicates how
components are wired and their configurations.

To transform those into real Docker configurations that we can run, we
invoke the following command:

```console
$ camp realize -d .
CAMP v0.1.0 (MIT)
Copyright (C) 2017, 2018 SINTEF Digital

Model loaded from './model.yml'.
Searching configurations in './out' ...
 - Building './out/config_3' ...
 - Building './out/config_4' ...
 - Building './out/config_1' ...
 - Building './out/config_2' ...

That's all folks!
```

We can see that CAMP has generate modified the template for each
configurations. For instance:

```console
$ tree out/config_1
out/config_1
├── configuration.dot
├── configuration.dot.png
├── configuration.yml
├── docker-compose.yml
└── images
	├── build_images.sh
	├── tomcat8_0
	│   └── Dockerfile
	└── xwiki8postgres_0
		├── docker-compose.yml
		├── Dockerfile
		├── Dockerfile~
		├── tomcat
		│   └── setenv.sh
		└── xwiki
			├── docker-entrypoint.sh
			└── hibernate.cfg.xml
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
