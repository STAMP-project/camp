# Stamp configuration sample on the Xwiki Use Case
Automatic generation of diverse configurations to test XWiki.

All the configurations are based on the same setting of XWiki deployment, i.e., a XWiki backend running in a Servlet container (Tomcat) and a JVM (OpenJDK), using an external database (either Postgres or MySQL). In addition, we employ a testing client to check the XWiki backend, using one simple test case: [the SuggestTest](https://github.com/xwiki/xwiki-platform/blob/master/xwiki-platform-distribution/xwiki-platform-distribution-flavor/xwiki-platform-distribution-flavor-test/xwiki-platform-distribution-flavor-test-misc/src/test/it/org/xwiki/test/misc/SuggestTest.java).
The client, the backend and the database are running in three separate docker containers.

The STAMP configuration amplifier will generate a set of images with different combinition of Tomcat and OpenJDK, e.g., Tomcat8.5 on OpenJDK9, Tomcat8.0 on OpenJDK8, etc. After that, the amplifier will generate a set of docker-compose files to further extend the configuration with different version of databases.

The objective is to generate minimal number of configurations to cover all the potential configuration aspects.

# Build the testing client
```bash build -t <your_client_image> ./util/client```

# Input
In order to generate reasonable configurations to test XWiki, we need the following input.

## Features
You first need to define a number of features, in [features.yml](features.yml). Each feature defines a special aspect you care about the configuration, such as java, application servier, database, etc. A feature can have sub features, such as different versions of a database. 

## Components to build docker images
The file [images.yml](images.yml) defines what images you need to host XWiki backend. The downloadingimages section defines the standard images from docker hub. The building rules defines different ways to build a new images on top of existing ones. For example, Tomcat7 is a building rule that needs an image that contains the "java" feature, and the new image will feature "tomcat7". Each rule needs a concrete Dockerfile in the [repo](repo) folder. These Dockerfiles can be either downloaded from the official repository or written by hand.

The mandatoryfeature property defines that we need an image that features xwiki.

Finally, we have an addtional constraint requiring that Tomcat7 and Tomcat8 cannot be build on top of OpenJDK9. Basred on our experiments, such compositions does not work.

## Template of docker-compose files
In the [docker-compose](docker-compose) folder, we need a [seed docker-compose file](docker-compose/docker-compose.yml) which defines the basic settings of the containers of client, backend and database. This sample seed template is based on the [official one recommended by XWiki](https://hub.docker.com/_/xwiki/). I combined the two files for MySQL and Postgres into a single file, and make the DB_HOST environment (Line 43) relevant the actually dependency. (NB: This is not necessary. A simpler solution is to give the same container\_name to the two database services, but it shows what we can do.) If the docker-compose file need addtional resource, just put it in the same folder.

# Run configuration testing amplification
```bash docker run -v $(pwd):/root/workingdir```

# Output
In this example, we generate four different images for the XWiki backend
- Xwiki8Mysql -> Tomcat85 -> OpenJdk8:
- Xwiki8Postgres -> Tomcat7 -> OpenJdk8
- Xwiki9Mysql -> Tomcat9 -> OpenJdk9
- Xwiki9Postgres -> Tomcat8 -> OpenJdk8
These four images covers all the features we defined on xwiki, tomcat and java.

You can build all the images by ```bash bash ./build/build.sh```

We also generate three docker-compose files, in the [docker-compose](docker-compose) folder. These files describes three different compositions of the the client, the backend and the database. Run one of them by ```bash docker-compose -f ./docker-compose/docker-compose-1.yml```.

The three configurations cover the following features, respectively:
- mysql5, xwiki9mysql, tomcat9, openjdk9
- tomcat7, openjdk8, xwiki8postgres, postgres10
- xwiki9postgres, tomcat8, postgres9, openjdk8

