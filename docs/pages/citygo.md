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
