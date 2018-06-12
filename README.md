## Table of contents
  - [What is CAMP?](#what-is-camp)
  - [Quick start](#quick-start)
  - [How does CAMP work?](#how-does-camp-work)
  - [CAMP Input](#camp-input)
  - [CAMP Output](#camp-output)
  - [Running CAMP on your project](#running-camp-on-your-project)

## What is CAMP?

CAMP (Configuration AMPlification) takes as input a sample testing configuration and generates automatically a number of diverse configurations. The generation is guided by predefined features and constraints, and utilizes a set of reusable pieces. The current version of CAMP is focused on the Docker environment, and the input and output configurations are specified as Dockerfiles or docker-compose files.

## Quick start
To get start, you need to copy the current repository:
```
git clone https://github.com/STAMP-project/camp 
```
Once copied, go to the docker folder to build a image that contains the tool:
```
cd docker/
docker build -t camp-tool:latest .
```
To run the tool, please go to the samples folder:
```
cd samples/xwiki
docker run -it -v $(pwd):/root/workingdir camp-tool:latest /bin/bash start.sh
```
The tool should produce four folders ```samples/xwiki/compose1```, ```samples/xwiki/compose2```, ```samples/xwiki/compose3```, ```samples/xwiki/compose3```. Each folder contains a docker compose file which a result of the amplification of the source compose file in ```samples/xwiki/docker-compose/docker-compose.yml```

## How does CAMP work
CAMP extract from the input Docker specifications an abstract configuration model, and and try to synthesis new models based on the features, variables and constraints. The figure below illustrates the approach:
![Alt text](src/docs/camp_idea.png "CAMP approach")
The new models will then be translate back into Docker specifications. These specifications can be executed in the same way as the original input, and therefore to replace the original testing configuration during either the manual testing or in a continuous integration pipeline.

## CAMP Input

The input to CAMP comprises two parts, i.e., the sample configuration and the scope definition.

The sample configuration, in the current set up, are Docker specifications, i.e., Dockerfiles and docker-compose files. A docker-compose file defines the architecture of a testing set-up, consisting of components for the application, the testing client, or the supportive services such databases. A Dockerfile defines how to build an image from a base one. Each of these components maps to a docker service in the docker-compose specification. The application itself may consist of multiple components, especially following a microservices architecture. Each docker service corresponds to an docker image. A docker image can be either directly downloaded (pulled) from a docker repository, such as the Docker Hub, or built locally. In the latter case, the CAMP users should provide a Dockerfile which defines how to build the image from a base one. If there are multiple images to be built locally, or an image can be built in alternative ways, the users should provide multiple Dockerfiles.


## CAMP Output

# Old README from here on, we will remove them gradually
# Configuration amplification based on Dockder


This folder contains the "generator" part as show in the following architecture.
It utilizes sample docker files (namely Dockerfile for images and docker-compose.yml for containers and their connections),
together with amplification result (abstract models), and generate new docker files.
![Alt text](doc/arch2.png "Generation framework architecture")

# Dockerfile generator
This generator takes the following two inputs:
- A repository of existing Dockerfiles, each in a seperate folder together with all the resources needed by it.
- A amplified model containing a number of stacks. Each stack indicate how to build a new image from the provided ones

The output is a new repository of generated Dockerfiles, each of which in a folder with all the required resources.
A build.sh script is also generated, so that a simple command ```bash ./build.sh``` could build all the images.

A usage is as below:
``` python src/dockerfilegen.py -i samples/images/java-python/result1.yml```

By default, the working directory is where that the input file locates.
In the directory, the "repo" folder contains the input Dockerfiles while the "build" folder contains the generation results.

TODO: The amplifier is not introduced yet.
If the generator invokes amplifier, then we do not need the inputfile, which is supposed to carry the amplification result.


# Docker compose generator

This generator takes one input, i.e., a seed docker-compose file, and generate a number of new files.

``` python src/composegen.py -i samples/compose/atos/docker-compo ```

The generator first extract an abstract model from the input compose.
We call this model *m0*
The model only contains the information that is interesting to the amplifier.
So far it includes only the services, the service name, the image name and the depends_on between services.
From *m0*, the amplifier will produce a number of new models, namely *m1*, *m2*, ..., *mn*.
In the example, we have three "generated models", as can be seen from Line 33 of [source code](src/composegen.py).
After that we merge each generated model back into the docker-compose file, based on "three-way comparison" and generate *n* new docker files.
