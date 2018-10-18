---
layout: default
---

# The CityGo Use-case

We describe here how to run CAMP on the CityGo use-case.

First, you need to fetch the CAMP sources, which contain the CityGo
example, using the following command:

```bash
$> git clone https://github.com/STAMP-project/camp 
```

The `samples/stamp/atos` directory contains the files that CAMP will
consume. To run camp (inside a Docker container), use the following
command:

```bash
$> docker run -it -v $(pwd)/samples/stamp/atos:/camp/workspace fchauvel/camp:latest camp generate -d workspace
``` 

CAMP generates two various configurations. Each configuration tweaks
parameters of the Apache server. The meta-model of CAMP specifies
variables. The variable is an abstraction which allows specifying
arbitrary modifications of docker files. In the given example, we
modify parameters of the docker-compose file in
`camp/samples/stamp/atos/docker-compose/docker-compose.yml`. In CityGo
there are two variables in `camp/samples/stamp/atos/images.yml`.

```yaml
...
buildingrules:
  Showcase:
    requires: [python]
    adds: [showcase]
    svar: [ThreadLimit, ThreadPerChild]
    depends: [postgres]
...
```

`ThreadLimit` defines a thread limit and `ThreadPerChild` specifies a
number of threads per child. These parameters are set for the backend
of the CityGo application. The file
`camp/samples/stamp/atos/variables.yml` specifies these variable and
possible values as follows.

```
ThreadLimit:
  ThreadLimit32:
    type: Int
    value: 128 
    operations:
      - substituion1:
          engine: regexp
          filename: "docker-compose.yml"
          placement: "ThreadLimit=64"
          replacement: "ThreadLimit=128"
ThreadPerChild:
  ThreadPerChildFree:
    type: Int
    operations:
      - substituion1:
          engine: regexp
          filename: "docker-compose.yml"
          placement: "ThreadsPerChild=25"
          replacement: "ThreadsPerChild=${value}"
...
```

In the example, each variable has one possible value, which does not
have to be the case. For each value, we have the `operations`
section. This section defines how a value should be realized. In the
given example, CAMP needs to perform a substitution operation on the
text file (`docker-compose.yml`). We replace `ThreadLimit=64`
with `ThreadLimit=128`. We also specify `type` and
`value`, which could be used by CAMP to define a proper value. We
can also leave it up to CAMP to decide a value, and then we just use a
placeholder which should be filled in,
e.g. `ThreadsPerChild=${value}`. CAMP decides values by evaluating
application constraints set up in
`camp/samples/stamp/atos/composite.yml`. To perform changes in
docker file, CAMP builds a product model by evaluating
constraints. The product model contains a list of references to
docker-compose files and list of variables with values to realize to
yield final compose files. You can find more examples with product and
realization models in `/camp/modules/camp-realize/`
