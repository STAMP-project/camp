---
layout: default
---

# The CityGo Use case


To execute CAMP on CityGo.
```
git clone https://github.com/STAMP-project/camp 
cd camp/docker/ && docker build -t camp-tool:latest .
cd ../samples/stamp/atos/ && docker run -it -v $(pwd):/root/workingdir camp-tool:latest /bin/bash allinone.sh
``` 
CAMP generates two various configurations. Each configuration tweaks parameters of the apache server. The meta-model of CAMP specifies variables. The variable is an abstraction which allows specifying arbitrary modifications of docker files. In the given example, we modify parameters of the docker-compose file in ```camp/samples/stamp/atos/docker-compose/docker-compose.yml```. In CityGo there are two variables in ```camp/samples/stamp/atos/images.yml```.
```
...
buildingrules:
  Showcase:
    requires: [python]
    adds: [showcase]
    svar: [ThreadLimit, ThreadPerChild]
    depends: [postgres]
...
```
```ThreadLimit``` defines a thread limit and ```ThreadPerChild``` specifies a number of threads per child. These parameters are set for the backend of the CityGo application. The file ```camp/samples/stamp/atos/variables.yml``` specifies these variable and possible values as follows.
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
In the example, each variable has one possible value, which does not have to be the case. For each value, we have the ```operations``` section. This section defines how a value should be realized. In the given example, CAMP needs to perform a substitution operation on the text file (```docker-compose.yml```). We replace ```ThreadLimit=64``` with ```ThreadLimit=128```. We also specify ```type``` and ```value```, which could be used by CAMP to define a proper value. We can also leave it up to CAMP to decide a value, and then we just use a placeholder which should be filled in, e.g. ```ThreadsPerChild=${value}```. CAMP decides values by evaluating application constraints set up in ```camp/samples/stamp/atos/composite.yml```. To perform changes in docker file, CAMP builds a product model by evaluating constraints. The product model contains a list of references to docker-compose files and list of variables with values to realize to yield final compose files. You can find more examples with product and realization models in ```/camp/modules/camp-realize/```
