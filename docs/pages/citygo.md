---
layout: default
---

# The CityGo Use-case

We describe here how to run CAMP on the CityGo use-case. In particular
we explain:

 1. The layout of the [required input files](#input_files);
 2. The [definition of variables in the CAMP model](#model);
 3. How to [generate configurations to cover all single variations](#coverage);
 4. How to [realize these configurations](#realize) so as to run them with docker.
 

The related files are available in the GitHub repository, under
`samples/citygo`.


```console
$ git clone https://github.com/STAMP-project/camp 
$ cd samples/stamp/atos
```

We assume hereafter that you already have CAMP up and running. If not,
please refer to [installation instructions](setup.html). Note that the
CityGo applications, is not open source, so you won't be able to
actually deploys and run it. We can however generate and realize the
configurations.

The CityGO application is a Python web application running on top of
the Django framework. The CityGo case-studies comes into flavours:
functionals and performance tests.

 * In the **functional** scenario, we run Selenium tests
 * In the **performance** scenaiorio, we run performance tests using
   CAMP's JMeter extension.


## The Performance Scenario

As explained above, in this scenario we run performance tests using
[JMeter](https://jmeter.apache.org/). The source files for this
scenario are available in the `samples/stamp/atos/performance`
directory.


<a name="perf-model"/>
### The CAMP Model

The main objective of this case study is to modify numerical
variables, which governs the configuration of the Apache server. In
the CAMP model (i.e., the file `camp.yml`), these variables are
attached to the "apache" component, although the substitution will
affect the Apache Server as defined in the docker-compose file.

The extract below show the `apache`component and its three
variables, namely `thread_limit`, `threads_per_child` and
`max_request_workers`.

```yaml
  [...]
  apache:
    provides_services: [ HttpProxy ]
    requires_services: [ CityGo ]
    variables:
      thread_limit:
        type: Integer
        values: [ 64, 128 ]
        realization:
          - targets: [ docker-compose.yml ]
            pattern: "ThreadLimit=64"
            replacements: [ ThreadLimit=64, ThreadLimit=128 ]
      threads_per_child:
        type: Integer
        values:
          range: [0, 128]
          coverage: 10
        realization:
          - targets: [ docker-compose.yml ]
            pattern: ThreadsPerChild=25
            replacements: ["ThreadsPerChild={value}"]
      max_request_workers:
        type: Integer
        realization:
          - targets: [ docker-compose.yml ]
            pattern: MaxRequestWorkers=150
            replacements: ["MaxRequestWorkers={value}"]
    implementation:
      docker:
        file: apache/Dockerfile
  [...]
```


### How to Generate All Configurations?

As for other case-studies, you can generate all possible
configurations with the following command:

```console
$ camp generate -d . --mode all
```

![CityGo
coverage]({{site.baseurl}}/assets/images/citygo_perf_all_configs.png
"The configurations that CAMP generates generates on the performance
scenario.")

In general, the presence of an unbound variable, such
`max_request_workers` entails *an infinte number of configurations*
Here however, there are only 10 configurations.

There are three variables:
 * `thread_limit`, which is either 64 or 128
 * `thread_per_child`, which ranges from 0 to 128, with a maximum
   coverage of 10. The actual values are therefore [0, 8, 16, 32, 40,
   48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128].
 * `max_request_worker` which is not bounded.

The CAMP model set the three following constraints:
 1. `thread_limit` > `thread_per_child`
 2. `thread_per_child` * 16 = `max_request_worker`
 3. (`thread_per_child` >= 100 and `max_request_worker` >= 200) or
    (`thread_limit` <= 64 and `max_request_worker` >= 2)

From Constraint 1 and the second part of Constraint 3, we know that
`thread_per_child`must be lower than thread_per_child, and therefore
strictly lower than 64. This reduces its possible values to the range
[0, 56]. From Constraint 2, `max_request_worker` must be above 2, and
also equals 16 * `thread_per_child`, which rules out the value 0,
leaving us with the range [8, 56].

From the first part of Constraint 1, we know that `thread_per_child`
must be above 100, which adds up the range [104, 112, 120, 128]. But
from Constraint 1, `thread_per_child` must strictly below
`thread_limit`, which invalidate value 128.

We are left with 10 possible values for `thread_per_child` that are
[8, 16, 24, 32, 40, 48, 56, 104, 112, 120]. In addition, we need one
configuration to test every single value, so we need 10
configurations.


<a name="coverage"/>
### How to Cover All Possible Variations?

To generate the set of configurations that cover all variations, we
use the following commands:


```console
$ camp generate -d . --mode covering
CAMP v0.1.0 (MIT)
Copyright (C) 2017, 2018 SINTEF Digital

Model loaded from './camp.yml'.
Searching for configurations ...

 - Config. 1 in './out/config_1/configuration.yml'.
   Includes python, postgres, showcase (104, 1664, 128), ubuntu

 - Config. 2 in './out/config_2/configuration.yml'.
   Includes python, showcase (112, 1792, 128), postgres, ubuntu

 ...

 - Config. 10 in './out/config_10/configuration.yml'.
   Includes python, showcase (32, 512, 64), postgres, ubuntu

That's all folks!
``` 

CAMP found 10 configurations with various values for the three
variables, all placed in the `out`directory:

```console
$ tree out
out
├── config_1
│   ├── configuration.dot
│   └── configuration.yml
├── config_2
│   ...
```

To better visualise these configurations, we can generate PNG images
using Graphviz and image magick as follows. The figure belows
illustrates these selected configurations.

```console
$ find . -name "*.dot" | xargs -I file dot -Tpng file -o file.png
$ find . -name "*.png" \
   | tr '\n' ' ' \
   | montage  -label '%d/%f' @- -geometry 300x300 configurations.png

```
<a name="realize" /> 
### How to Realize these Configurations?

CAMP has generated abstract configurations in the `out` folder. This means that CAMP
has so far only generated a YAML file for each configuration. This YAML file only indicates how
components are wired together and configured (i.e., variable
settings). Those abstract configurations cannot be directly executed or deployed. CAMP first needs to "*realize*" them i.e. to link 
them to concrete, deployable artifacts (Docker configurations).

To transform abstract CAMP configurations into concrete Docker configurations which we can run,
we first need to fill the template directory with means to deploy
every component listed in the `camp.yml` file.

---

> **Note** CAMP and docker-compose both describes service
orchestrations, but they work at *different granularity*
levels. docker-compose only bind together services and assumes that
each service is a Docker image. By contrast, CAMP works with
components that it assembles into software stacks, each stacks
becoming a service, running in a separate container, as in the
docker-compose file.

So the `template` directory must contains a docker-compose file, whose
services must point towards the "top" component of each software
stacks that CAMP generate.

---

So if we look at one specific abstract configuration that CAMP has generated,
say Config 1 for instance, we see that Container 2 includes several
components, that is citygo, running on top of python, running on top
of ubuntu.

![]({{site.baseurl}}/assets/images/citygo_perf_config_1.png "The first
configuration generated by CAMP on the 'performance' scenario").

As usual, the template directory must provide installation material
for every component of the `camp.yml` that is not implemented by a
pre-existing Docker image. We therefore omit both the `hub` component
and the `ubuntu` component.

We therefore create the following structure:

```console
$ tree template -L 2
template
├── apache
│   ├── demo_site.conf
│   ├── Dockerfile
│   └── mpm_event.conf
├── browser
│   ├── Dockerfile
│   └── tests.py
├── citygo
│   └── Dockerfile
├── docker-compose.yml
├── postgres
│   ├── Dockerfile
│   ├── init-db.sql
│   └── postgresql.conf
└── python
    └── Dockerfile
```

In Container 2, CAMP will reassemble the components by creating an
image where python is deployed on top of ubuntu, and then another
image where the citygo app is deployed on top of those two. To do so
we need Dockerfile with specific `FROM` statements that CAMP can
override to assemble the component as it needs. For instance the
Dockerfile of the citygo component looks like:

```dockerfile
FROM camp/runtime

# Describe here how to install Citygo only. CAMP will replace the
# 'FROM' statement so that it points to an image that already includes
# both Python and Ubuntu.

RUN apt-get updrade \
    && ...
```

CAMP searches for FROM statements whose image name starts with
`camp/`. By convention, we use 'camp/runtime', to emphasize that the
FROM statement that CAMP will override at runtime.

Now, the services in the template 'docker-compose' must points towards
single components in the template directory. When a service in the
docker-compose file match a 'stack' assembled by CAMP, the
docker-compose file must point towards the top component of the
stack. For instance, in Container 2, the citygo service must point to
the citygo component. For instance:

```yaml
  web:
    build: ./citygo
    container_name: "my_web"
    restart: always
    environment:
      - DJANGO_SETTINGS_MODULE=citygo_settings.settings
      - BROWSERNAME=chrome
```



Once the template directory contains all needed material to deploy all
individual component, and the docker-compose file is consistent, we
can invoke CAMP generate using the following command:

```console
$ camp realize -d .
CAMP v0.6.3 (MIT)
Copyright (C) 2017 -- 2019 SINTEF Digital

Model loaded from './camp.yml'.
Searching configurations in './out' ...
 - Building './out/config_5' ...
 - Building './out/config_3' ...
 - Building './out/config_7' ...
 - Building './out/config_4' ...
 - Building './out/config_1' ...
 - Building './out/config_8' ...
 - Building './out/config_6' ...
 - Building './out/config_9' ...
 - Building './out/config_10' ...
 - Building './out/config_2' ...

That's all folks!
```

We can see that CAMP has generated modified the template for each
configurations. For instance:

```console
$ tree -L 3 out/config_1
out/config_1
├── configuration.dot
├── configuration.yml
├── docker-compose.yml
└── images
    ├── apache_0
    │   ├── demo_site.conf
    │   ├── Dockerfile
    │   └── mpm_event.conf
    ├── browser_0
    │   ├── Dockerfile
    │   └── tests.py
    ├── build_images.sh
    ├── citygo_0
    │   └── Dockerfile
    ├── postgres_0
    │   ├── Dockerfile
    │   ├── init-db.sql
    │   └── postgresql.conf
    └── python_0
        └── Dockerfile
```

Note that CAMP has generated a specific shell script
`build_images.sh`, which it will use to build the images needed for
Container 2. 

```sh
#!/bin/bash
#
# Generated by CAMP. Edit carefully
#
# Build all images and set the appropriate tags
#
set -e
docker build --no-cache -t camp-python_0 ./python_0
docker build --no-cache -t camp-citygo_0 ./citygo_0
echo 'All images ready.'
```

Above, we see that this script will create images with specific tags
and that this tags are placed into the `FROM` statement of the related
Dockerfiles. For instance, the Dockerfile of the `citygo_0` component
contains:


```dockerfile
FROM camp-python_0

# Describe here how to install Citygo only. CAMP will replace the
# 'FROM' statement so that it points to an image that already includes
# both Python and Ubuntu.

RUN apt-get updrade \
    && ...
```

## The Functional Scenario

In the functional tests scenario, we focus on injecting architectural
changes. We replace Apache with NGinx, we switch between alternative
versions of both the Django framework and PostgresSQL database. We
options we select are:

 - Use either Django 1.10.1 or Django 2.2.6
 - Use either PostgresSQL 9.3, 10 or 11
 - Use either Apache or NGinx as a proxy
 - Activate or not the GZip option of the NGinx proxy
 

### Modelling Variations in `camp.yml`

To keep things simple, we model change of version using
variables. For instance, we add a variable named `django` to the
`citygo` component, as follows.


```yaml
  citygo:
    provides_services: [ CityGo ]
    requires_services: [ Postgres, Mongo ]
    requires_features: [ Python ]
    variables:
      django:
        values: [ v1.10.2, v2.2.6 ]
```

We proceed in the same way for Postgres and for the option of the
NGinx proxy.

Switching between Apache or NGinx translates in both component having
the same signature: Both the `apache` and the `nginx` component provides
the `HttpProxy` service and requires the `CityGo` service. 

```yaml
  nginx:
    provides_services: [ HttpProxy ]
    requires_services: [ CityGo ]
    variables:
      gzip:
        values: [on, off]
    implementation:
      docker:
        file: nginx/Dockerfile

  apache:
    provides_services: [ HttpProxy ]
    requires_services: [ CityGo ]
    implementation:
      docker:
        file: apache/Dockerfile
```

### Generating Configurations

As shown in the figure below, camp generates 18 configurations using
the followings command. We omit parts of the output for the sake of
brevity.

```console
$ camp generate -d . --mode all
CAMP v0.6.3 (MIT)
Copyright (C) 2017 -- 2019 SINTEF Digital

Loaded './camp.yml'.

 - Config. 1 in './out/config_1/configuration.yml'.
   Includes ubuntu, citygo (v1.10.2), apache, hub, postgres (v9), mongo, br...

[...]

 - Config. 18 in './out/config_18/configuration.yml'.
   Includes ubuntu, nginx (True), citygo (v2.2.6), hub, mongo, browser, pos...
   
That's all folks!
```

![]({{site.baseurl}}/assets/images/citygo_func_all_configs.png
"Configurations that CAMP founds in the functional tests scenarios").


### Generation of a Covering Array

We may not be interested in testing every single
configurations. Instead we may prefer to test every single options at
least once. This finding a smaller number of configurations that use
the two versions of Django, both apache and nginx, as well as the
three version of Postgres.

CAMP can do this by computing a "covering array", that is a small set
of configuration where each option is used at least once. This yields
5 configurations. To do so, we proceed as follows

```console
$ camp  generate -d . --mode covering
CAMP v0.6.3 (MIT)
Copyright (C) 2017 -- 2019 SINTEF Digital

Loaded './camp.yml'.

 - Config. 1 in './out/config_1/configuration.yml'.
   Includes ubuntu, hub, python, postgres (v9), citygo (v1.10.2), browser, ...

 - Config. 2 in './out/config_2/configuration.yml'.
   Includes ubuntu, citygo (v2.2.6), hub, python, postgres (v10), browser, ...

 - Config. 3 in './out/config_3/configuration.yml'.
   Includes ubuntu, citygo (v2.2.6), hub, postgres (v11), python, browser, ...

 - Config. 4 in './out/config_4/configuration.yml'.
   Includes ubuntu, citygo (v2.2.6), hub, postgres (v11), python, browser, ...

 - Config. 5 in './out/config_5/configuration.yml'.
   Includes ubuntu, hub, python, citygo (v1.10.2), postgres (v10), browser,...

That's all folks!
```

![]({{site.baseurl}}/assets/images/citygo_func_cov_configs.png
"Configurations that CAMP founds in the functional tests scenarios").


### Realisation of the Configurations

At first CAMP generates only models of configurations (as YAML
files). To obtain deployable configurations, we must complete the
variation model and detail how each variation must be enacted.


### Switching Versions of Postgres

The version of Postgres we use is setup in the [associated
DockerFile](https://github.com/STAMP-project/camp/blob/master/samples/stamp/atos/functional/template/postgres/Dockerfile),
more precisely, in the `FROM` statement. We can switch version of
postgres by simply modifying this FROM statement. We can therefore
realise the variable we have created in the `postgres` component
using a substitution, as follows:

```yaml
  postgres:
    provides_services: [ Postgres ]
    variables:
      version:
        values: [v9, v10, v11]
        realization:
          - targets: [ "postgres/Dockerfile" ]
            pattern: "FROM postgres:9.3"
            replacements:
              - "FROM postgres:9.3"
              - "FROM postgres:10"
              - "FROM postgres:11"
```

Here, each value is associated with a different `FROM` statement. This
realisation tells CAMP to search for the pattern `FROM postgres:9.3`
and to substitute it with the adequate replacement (replacements must
be ordered according to the variable's values).

### Switching Version of Django

The Django framework comes as Python library, which is downloaded when
we install the CityGo application. The version of the Django framework
thus written down in the file [`requirements.txt`](), which defines
the dependencies, as in the following example:

```
Django==1.10.2
django-allauth==0.27.0
django-rest-auth==0.8.1
djangorestframework==3.4.7
httplib2==0.9.2
oauth2==1.9.0.post1
oauthlib==2.0.0
psycopg2
psycopg2-binary
python-openid==2.2.5
requests>=2.18.2
requests-cache==0.4.12
```

We can therefore switch between versions of Django by replacing the
fragment `Django==1.10.2`. We do so by defining the realisation of the
`citygo` component as a substitution:

```yaml
  citygo:
    provides_services: [ CityGo ]
    requires_services: [ Postgres, Mongo ]
    requires_features: [ Python ]
    variables:
      django:
        values: [ v1.10.2, v2.2.6 ]
        realization:
          - targets: [ citygo/requirements.txt ]
            pattern: "Django==1.10.2"
            replacements:
              - "Django==1.10.2"
              - "Django==2.2.6"
```

### Switching between Apache and NGinx

To switch between Apache and NGinx requires to modify the service
orchestration, and in turn, the docker-compose file. To do so, we
define two docker-compose file and we select the correct one when a
given component is selected.

```yaml
  apache:
    provides_services: [ HttpProxy ]
    requires_services: [ CityGo ]
    implementation:
      docker:
        file: apache/Dockerfile
    realization:
      - select: docker-compose-apache.yml
        instead_of:
          - docker-compose-nginx.yml
        as: docker-compose.yml
```

With this realisation, attached to the Apache component, when CAMP
realises a configuration that includes this component, it will select
the file named `docker-compose-apache.yml` as the `docker-compose.yml`
and discards the other one.

We proceed in the same way for the NGinx component:

```yaml
  nginx:
    provides_services: [ HttpProxy ]
    requires_services: [ CityGo ]
    variables:
      gzip:
        values: [on, off]
    implementation:
      docker:
        file: nginx/Dockerfile
    realization:
      - select: docker-compose-nginx.yml
        instead_of:
          - docker-compose-apache.yml
        as: docker-compose.yml

```


### Activating GZip on NGinx

The GZip option is actually set as an environment variable passed to
associated container, through the `docker-compose.yml` descriptor. We
can therefore simply search for the pattern `gzip=on` and replace it
when needed, as follows:

```yaml
  nginx:
    provides_services: [ HttpProxy ]
    requires_services: [ CityGo ]
    variables:
      gzip:
        values: [on, off]
        realization:
          - targets: [ docker-compose.yml ]
            pattern: "gzip=on"
            replacements:
              - gzip=on
              - gzip=off
    implementation:
      docker:
        file: nginx/Dockerfile
```


Once all the possible option are realize, we can build the
configurations as follows:

```console
$ camp realize -d .
CAMP v0.6.3 (MIT)
Copyright (C) 2017 -- 2019 SINTEF Digital

Loaded './camp.yml'.
Loading configurations from './out' ...
 - Built configuration './out/config_1.
 - Built configuration './out/config_2.
 - Built configuration './out/config_4.
 - Built configuration './out/config_3.
 - Built configuration './out/config_5.

That's all folks!
```
