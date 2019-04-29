---
layout: default
---

# CAMP Execute

The command `camp execute` runs your integration tests on all the
generated configurations (see camp generate and camp realize).


```bash
$ camp execute ...
```

CAMP will go in each configurations, build the needed images, deploy
the orchestration using docker-compose, runs the tests, and collect
the test reports.

Here is the usage and options:
```console
$ camp execute --help
usage: CAMP execute [-h] [-d WORKING_DIRECTORY] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -d WORKING_DIRECTORY, --directory WORKING_DIRECTORY
                        the directory that contains the input files
  -s, --simulated       Display but do NOT execute the commands that CAMP triggers
```

---
**Note:** `CAMP execute` *requires* that docker be up and running.
---


## Example: Test A Java WebApp

If you are unsure about how to generate new configuration with CAMP,
please check the camp generate and camp realize commands.

Let us consider a [Java
WebApp](http://github.com/stamp-project/camp/tree/master/samples/java) as a
running example of CAMP execute. We called it "Greetings" as
it simply returns a greeting message.

Here is an overview of our project structure:

```console
$ tree
.
├── camp.yaml
└── template
    ├── docker-compose.yml
    ├── greetings
    │   ├── Dockerfile
    │   ├── pom.xml
    │   └── src
    │       └── main
    │           ├── java/org/samples
    │           │            └── GreetingService.java
    │           └── webapp/WEB-INF
    │                      └── web.xml
    └── tests
        ├── Dockerfile
        ├── pom.xml
        └── src/test/java/org/samples
                              └── GreetingServiceTest.java
```

Greetings is a simple REST service running on top of a Tomcat
server. It comes with an integration test, placed into a separate
Maven project. The docker-compose file provides an example of
deployment including both the integration test and the service.

### The CAMP Model

Let's first look at the [CAMP
model](http://github.com/stamp-project/camp/tree/master/samples/java/camp.yaml),
where we specify how to change the underlying version of the Tomcat
application server, as in the following excerpt:

```yaml
  greetings:
    provides_services: [ Greetings ]
    variables:
      tomcat:
        values: [ v7, v8, v9 ]
        realization:
         - targets: [ greetings/Dockerfile ]
           pattern: "tomcat:8-jre8"
           replacements:
             - tomcat:7-jre8
             - tomcat:8-jre8
             - tomcat:9-jre8
    implementation:
      docker:
        file: greetings/Dockerfile
```

To execute the tests on the configuration that CAMP has generated, we
need to explain how to run these tests. We thus elaborate on the
`tests` component, which contains our integration test.

```
  tests:
    provides_services: [ IntegrationTests ]
    requires_services: [ Greetings ]
    implementation:
      docker:
        file: tests/Dockerfile
    tests:
      command: mvn -B test
      reports:
        format: junit
        location: target/surefire-reports
        pattern: .xml
```

Note the new `tests` section that describes the command to be run,
that is `mvn -B test`. as well as the expected format of the test
reports, their location, and the extension used to detect them.

---
**Warning**: As per version 0.3, CAMP only supports JUnit/XML test
reports.
---


### The Deployment Template

CAMP requires a template deployment, which it will modifies according
to the given CAMP model.

As you can see in our project structure, our [deployment
template](http://github.com/stamp-project/camp/tree/master/samples/java/template)
contains the code source for both the Greeting service and its
integration test, along with Dockerfile that specify how to build and
install this pieces of software.

#### The Greeting Service

Our greetings service is simple Jersey REST service. Here the Java
code of the REST end point, but we also have the necessary
[`web.xml`](http://github.com/stamp-project/camp/tree/master/samples/java/template/greetings/src/main/webapp/WEB-INF/web.xml)
to specify servlets' bindings and the [Maven POM
file](http://github.com/stamp-project/camp/tree/master/samples/java/template/greetings/pom.xml)
to build the project.

```java
@Path("/hello")
public class GreetingService {

    @GET
    @Path("/{name}")
    public Response getMessage(@PathParam("name") String name) {
        final String output = String.format("Hello '%s'!", name);
        return Response.status(200).entity(output).build();
    }

}
```

#### A Simple Integration Test

We also wrote a single integration test, in a separate Maven project,
which simply calls our Greeting service and check whether it gets and
HTTP OK as a response. Here is the code of the test:

```java
static final String END_POINT = "http://greetings:8080/greetings/rest/hello/%s";

@Test
public void testStatusCode() throws Exception {
    URL resource = new URL(String.format(END_POINT, "franck"));
    HttpURLConnection connection = (HttpURLConnection) resource.openConnection();

    int responseCode = connection.getResponseCode();

    assertEquals(200, responseCode);
}
```


### Running CAMP Execute

To run camp execute, you must already have generated and realized the
configuration. On this Java example, CAMP generates three
configurations, one per version of Tomcat.

```console
$ camp generate -d .
$ camp realize -d .
$ camp execute -d .
CAMP v0.3.3 (MIT)
Copyright (C) 2017 -- 2019 SINTEF Digital

Loaded './camp.yaml'.
Loading configurations from './out' ...

 - Executing ./out/config_1
   1. Building images ...
      $ bash build_images.sh (from './out/config_1/images')
   2. Starting Services ...
      $ docker-compose up -d (from './out/config_1')
   3. Running tests ...
      $ docker-compose run tests mvn -B test (from './out/config_1')
   4. Collecting reports ...
      $ docker ps --all --quiet --filter name=config_1_tests_run_1 (from './out/config_1')
      $ docker cp f68e14d053a6:/tests/target/surefire-reports ./test-reports (from './out/config_1')
      Reading TEST-org.samples.GreetingServiceTest.xml
   5. Stopping Services ...
      $ docker-compose down (from './out/config_1')

 - Executing ./out/config_2
   1. Building images ...
      $ bash build_images.sh (from './out/config_2/images')
   2. Starting Services ...
      $ docker-compose up -d (from './out/config_2')
   3. Running tests ...
      $ docker-compose run tests mvn -B test (from './out/config_2')
   4. Collecting reports ...
      $ docker ps --all --quiet --filter name=config_2_tests_run_1 (from './out/config_2')
      $ docker cp 0d71c0372058:/tests/target/surefire-reports ./test-reports (from './out/config_2')
      Reading TEST-org.samples.GreetingServiceTest.xml
   5. Stopping Services ...
      $ docker-compose down (from './out/config_2')

 - Executing ./out/config_3
   1. Building images ...
      $ bash build_images.sh (from './out/config_3/images')
   2. Starting Services ...
      $ docker-compose up -d (from './out/config_3')
   3. Running tests ...
      $ docker-compose run tests mvn -B test (from './out/config_3')
   4. Collecting reports ...
      $ docker ps --all --quiet --filter name=config_3_tests_run_1 (from './out/config_3')
      $ docker cp 96202e3e3aa5:/tests/target/surefire-reports ./test-reports (from './out/config_3')
      Reading TEST-org.samples.GreetingServiceTest.xml
   5. Stopping Services ...
      $ docker-compose down (from './out/config_3')

Test SUMMARY:

Configuration                 RUN   PASS   FAIL  ERROR
-------------------------------------------------------
./out/config_1                  1      1      0      0
./out/config_2                  1      1      0      0
./out/config_3                  1      1      0      0
-------------------------------------------------------
TOTAL                           3      3      0      0

That's all folks
```
