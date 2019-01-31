# Proactive CAMP sample

In the context of the project STAMP, ActiveEon is a use case to explore several
configuration notably for using different databases. This readme explain show
how to run camp for proactive worflows & schedulling.

## Building camp last version


To build camp go to project root and use:

```bash
docker build . -t camp
```

To run camp within the created image use.

```bash
docker run -it camp bash
```

Work whithin the docker container has some drawbacks. The changes on the current
drive are not seem or either presistent. Alternatively, you can also use a
mounting point so camp container access an outside folder.


```bash
docker run -t -v $PWD:/campworkingdir camp camp -h
```

Now you can proceed to use camp. For instance for this example change current
directory to be `samples/stamp/activeeon` and then run:

```bash
docker run -t -v $PWD:/campworkingdir camp camp generate -d /campworkingdir
```

You can clean exited container and unlinked images using:

```bash
docker system prune
```

## Getting proactive from jenkins

Visit your jenkins site to get the the api-token first.

```bash
http://<yourserver>/user/<username>/configure

curl --silent --show-error http://<username>:<api-token>@<jenkins-server>/job/<job-name>/doDelete
```

## Getting system tests

* See with Fabien, is it a single test or all?

* How to run the tests within camp? see with Franck Chauvel


## Todo

* Entrypoint.sh that find and call proactive server `/root/proactive/bin/proactive-server`

* After `docker-compose up` on `config_0`, we must have 2 containers running:
  - 1 mysql-camp
  - 2 proactive server


* Change the configuration of proactive-server to use the mysql databases see References

## References

* Proactive docker container to target system tests;

  - The last build proactive artifact [here](http://jenkins.activeeon.com/view/NightlyRelease/job/nightly-release/lastSuccessfulBuild/artifact/build/distributions/)

  - The system tests project is [here](https://bitbucket.org/activeeon/scheduling-system-tests/src/master/)

  - Example of running proactive system tests [here](http://jenkins.activeeon.com/job/scheduling-system-tests/)

* Add database intial setup;

  - Mysql database configuration [here](https://docs.google.com/document/d/1z9qNB64Sch3n-F5dwgFCmbKzKXSqfjfjYD9PLmSsgsM/edit#heading=h.1qei06ddonzh)

  - Mysql connector [here](https://dev.mysql.com/downloads/connector/j/)

  - Postgres database configuration [here](https://docs.google.com/document/d/1z9qNB64Sch3n-F5dwgFCmbKzKXSqfjfjYD9PLmSsgsM/edit#heading=h.1qei06ddonzh)

  - Postgres connector [here](https://jdbc.postgresql.org/download.html)

* Change database configuration for proactive image;

* Run with the 2 selected databases;

* Collect performance measures : memory, cpu, security;
