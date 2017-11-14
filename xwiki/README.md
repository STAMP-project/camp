# Stamp configuration sample on the Xwiki Use Case
Automatic generation of diverse configurations to test XWiki.

All the configurations are based on the same setting of XWiki deployment, i.e., a XWiki backend running in a Servlet container (Tomcat) and a JVM (OpenJDK), using an external database (either Postgres or MySQL). In addition, we employ a testing client to check the XWiki backend, using one simple test case: [the SuggestTest](https://github.com/xwiki/xwiki-platform/blob/master/xwiki-platform-distribution/xwiki-platform-distribution-flavor/xwiki-platform-distribution-flavor-test/xwiki-platform-distribution-flavor-test-misc/src/test/it/org/xwiki/test/misc/SuggestTest.java).
The client, the backend and the database are running in three separate docker containers.

The STAMP configuration amplifier will generate a set of images with different combinition of Tomcat and OpenJDK, e.g., Tomcat8.5 on OpenJDK9, Tomcat8.0 on OpenJDK8, etc. After that, the amplifier will generate a set of docker-compose files to further extend the configuration with different version of databases.

# Build the testing client
```bash build -t <your_client_image> ./util/client```

# Input
In order to generate reasonable configurations to test Xwiki

# Run configuration testing amplification
```bash docker run -v /home//stamp-samples/xwiki:/root/workingdir```

All the images
