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
