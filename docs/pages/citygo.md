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
please refer to [installation instructions](setup.html).

<a name="input_files"/>
## The Input Files

Here is the structure of the `citygo` directory, which contains both
the CAMP model and the tenplate orchestrations.

```bash
$ tree
├── camp.yml
└── template
    ├── docker-compose.yml
    ├── postgres
    │   ├── Dockerfile
    │   └── postgresql-template.conf
    └── showcase
        ├── Dockerfile
        ├── mpm_prefork-template.conf
        └── mpm_worker-template.conf
```

<a name="model"/>
## The CAMP Model

The main objective of this case study is to modify numerical
variables, which governs the configuration of the Apache server. Note
that, in the CAMP model (i.e., the file `camp.yml`), these variables
are attached to the "showcase" component, although the substitution
will affect the Apache Server as defined in the docker-compose file.

The extract below show the `showcase`component and its three
variables, namely `thread_limit`, `threads_per_child` and
`max_request_workers`.

```yaml
  [...]
  showcase:
    provides_services: [ Showcase ]
    requires_services: [ Postgres ]
    requires_features: [ Python ]
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
        file: repo/showcase/Dockerfile
  [...]
```


## How to Generate All Configurations?

As for other case-studies, you can generate all possible
configurations with the following command:

```console
$ camp generate -d . --all
```

Note however that the variable `max_request_workers` is not directly
constrained, and this entails *a very large number of configurations*.


<a name="coverage"/>
## How to Cover All Possible Variations?

To generate the set of configurations that cover all variations, we
use the following commands:


```console
$ camp generate -d . --coverage
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
![CityGo coverage]({{site.baseurl}}/assets/images/citygo_coverage.png "The configurations that CAMPS generate to cover the CityGo case")


<a name="realize" /> 
## How to Realize the Configurations?

CAMP has generated configuration in the `out`. But so far, CAMP only
generates a YAML file for each configuration that indicates how
components are wired and their configurations.

To transform those into real Docker configurations which we can run,
we invoke the following command:

```console
$ camp realize -d .
CAMP v0.1.0 (MIT)
Copyright (C) 2017, 2018 SINTEF Digital

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
    ├── postgres_0
    │   ├── Dockerfile
    │   └── postgresql-template.conf
    └── showcase_0
        ├── Dockerfile
        ├── mpm_prefork-template.conf
        └── mpm_worker-template.conf
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
