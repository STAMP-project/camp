---
layout: default
---

# CAMP Generate

CAMP generate amplify the test configuration. It generates new
configuration where both the stacks and the orchestration have been
modified. The stacks are images that run withing Docker container,
whereas the orchestrations are compositions of services that we
defined in docker-compose files.


Here is the tyical directory structure that CAMP generate
expects. There are three main configuration files, which must appear at
the root of our working directory.

1. `features.yml`
2. `images.yml`
3. `composite.yml`

Here is the structure of our workspace:

```bash
workspace
├── composite.yml            # Controls the amplication of orchestrations
├── docker-compose
│  ├── docker-compose.yml    # The service orchestration to amplify
│  └── xwiki.cnf
├── features.yml             # Defines the features and their variants
├── images.yml               # Control the amplications of stacks
└── repo                     # Contains a directory per feature variants
    ├── Tomcat7
    ├── Tomcat8
    ├── Tomcat85
    ├── Tomcat9
    ├── Xwiki8Mysql
    ├── Xwiki8Postgres
    ├── Xwiki9Mysql
    └── Xwiki9Postgres
```

## Generating the Configurations
To generate the new configurations, simply run the following command:

```bash
$> camp generate -d workspace 
```

CAMP will then create two new directories namely `out`and `build`,
that contains the new configurations.


## Defining the Features
We define the feature in a YAML file called `features.yml`, placed at
the root of the working directory. This file is needed both for the
amplification of stacks and orchestrations. Here is an example from the
XWiki case.

```yml
java:
  openjdk:
    - openjdk9
    - openjdk8

appsrv:
  tomcat:
    - tomcat7
    - tomcat8
    - tomcat85
    - tomcat9
    
db:
  mysql:
    - mysql8
    - mysql5
  postgres:
    - postgres9
    - postgres10

xwiki:
  - xwiki9mysql
  - xwiki9postgres
  - xwiki8mysql
  - xwiki8postgres
``` 

It defines what are the features inside our configurations. One may
read it as: "There is a "db" feature, which is either a `mysql` or
`postgres` and so one and so forth.

## Amplifying Stacks

The file `images.yml` controls the amplication of stacks, that is the
generation of new Docker images.

This file defines which features are based on remote images (that
should be downloaded), as well as the dependencies (in terms of
features) between the images. The section `buildingrules` captures
these dependencies.

Note that all the feature that are not downloaded, should be found in
the `repo` subdirectory.

```yaml
downloadimages:
  OpenJdk8:
    features: [openjdk8]
    name: openjdk
    tag: 8
  OpenJdk9:
    features: [openjdk9]
    name: openjdk
    tag: 9
buildingrules:
  Tomcat7:
    requires: [java]
    adds: [tomcat7]
  Tomcat8:
    requires: [java]
    adds: [tomcat8]
  Tomcat85:
    requires: [java]
    adds: [tomcat85]
  Tomcat9:
    requires: [java]
    adds: [tomcat9]
  Xwiki9Mysql:
    requires: [tomcat]
    adds: [xwiki9mysql]
    depends: [mysql]
  Xwiki9Postgres:
    requires: [tomcat]
    adds: [xwiki9postgres]
    depends: [postgres]
  Xwiki8Mysql:
    requires: [tomcat]
    adds: [xwiki8mysql]
    depends: [mysql]
  Xwiki8Postgres:
    requires: [tomcat]
    adds: [xwiki8postgres]
    depends: [postgres]
mandatoryfeature: [xwiki]
constraints:
  - BuildImage.forall(e1, Implies(Or(bi1.using == rules['Tomcat7'], bi1.using == rules['Tomcat8']), Not(bi1['from'].features.contains(features['openjdk9']))))"
```

## Amplifying Orchestrations

The files `composite.yml` defines how the orchestrations are
generated. Here is an example of the one used in the XWiki case.

```yaml
services:
  web:
    imgfeature: [xwiki]
    mandatory: true
  mysql:
    imgfeature: [mysql]
  postgres:
    imgfeature: [postgres]

images:
  Mysql5: {name: mysql, tag: "5", features: [mysql5]}
  Mysql8: {name: mysql, tag: "8", features: [mysql8]}
  Postgres9: {name: postgres, tag: "9", features: [postgres9]}
  Postgres10: {name: postgres, tag: "10", features: [postgres10]}

constraints:
  - Not(services['mysql'].alive() == services['postgres'].alive())
  - services['web'].alive()
```

The `services` section specifies the features offered by each services
in the docker-compose file (by convention
`docker-compose/docker-compose.yml`).

The `images`section defines additional images (besides those defined
to amplified stacks) that can be used. Each images specify its name
and tag (to be pulled from remote repositories) as well as the feature
it will provide.

Eventually, the `constraints` section adds some rules to invalidate
specific orchestrations.
