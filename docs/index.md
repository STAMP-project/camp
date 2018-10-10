---
layout: default
---

# What is CAMP?
CAMP (Configuration AMPlification) takes as input a sample testing configuration and generates automatically a number of diverse configurations. The generation is guided by predefined features and constraints, and utilizes a set of reusable pieces. The current version of CAMP is focused on the Docker environment, and the input and output configurations are specified as Dockerfiles or docker-compose files.

# Quick start
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
cd samples/stamp/xwiki
docker run -it -v $(pwd):/root/workingdir camp-tool:latest /bin/bash start.sh
```
The tool should produce four folders ```samples/xwiki/compose1```, ```samples/xwiki/compose2```, ```samples/xwiki/compose3```, ```samples/xwiki/compose3```. Each folder contains a docker compose file which is a result of the amplification of the source compose file in ```samples/xwiki/docker-compose/docker-compose.yml```

## How does CAMP work
CAMP extracts from the input Docker specifications an abstract configuration model, and tries to synthesize new models based on the features, variables and constraints. The figure below illustrates the approach:
![Alt text](assets/images/camp_idea.png "CAMP approach")
The new models will then be translated back into Docker specifications. These specifications can be executed in the same way as the original input, and therefore to replace the original testing configuration during either the manual testing or in a continuous integration pipeline.

## CAMP Input/Output
The input to CAMP comprises two parts, i.e., the sample configuration and the scope definition. The sample configuration, in the current set up, are Docker specifications, i.e., docker files and docker-compose files. A docker-compose file defines the architecture of a testing set-up, consisting of components for the application, the testing client, or the supportive services such databases. A docker file defines how to build an image from a base one. Each of these components maps to a docker service in the docker-compose specification. The application itself may consist of multiple components, especially following a micro-service architecture. Each docker service corresponds to an docker image. A docker image can be either directly downloaded (pulled) from a docker repository, such as the Docker Hub, or built locally. In the latter case, the CAMP users should provide a docker file which defines how to build the image from a base one. If there are multiple images to be built locally, or an image can be built in alternative ways, the users should provide multiple docker files.

CAMP outputs a set of specifications, docker files, and docker-compose files.
- ```camp/samples/stamp/xwiki/out/genimages.yml``` defines a chain of rules to evaluate to build new docker images
- ```camp/samples/stamp/xwiki/out/ampimages.yml``` lists docker images with labels to generate
- ```camp/samples/stamp/xwiki/out/ampcompose.yml``` lists docker-compose files to build from the template
- ```camp/samples/stamp/xwiki/build/``` contains folder with generated docker files
- ```camp/samples/stamp/xwiki/build/build.sh``` is a script to build images from generated docker files

## Examples
In the samples directory of the repository, there are two examples. 

In the first example, we have set up CAMP to test an open-source project XWiki. XWiki is an ultimate wiki platform to facilitate collaborative process inside any organization. XWiki can be in principle set up in various environments and various configurations. CAMP provides means to capture this variations in environment and configurations, generate those different environments and configurations. CAMP also facilitates testing against those generated configurations.

In the second example, CAMP is set up against a CityGo application by ATOS. CityGo can be set up in various environments and configurations. In this example, we demonstrate how CAMP can vary not just elements which map to docker images and services, but also arbitrary parameters and commands in docker files.



# Running CAMP on your project

To set CAMP on your project. There are two prerequisites:
* Your project should be dockerised.
* New configuration of the project can be achieved by:
  * By substituting the FROM statement of a Dockerimage file
  * By substituting an image of a docker-compose file

Further, we need to identify variation points of your configuration, e.g., java versions. We fill out feature.yml with this information. We also need to define building rules which are used to build new docker files. This information is filled in images.yml file. This allows generating various docker files which are various possible configuration of your application. If we need to generate various docker-compose file, we need to fill in compose.yml. However, this is optional. 
