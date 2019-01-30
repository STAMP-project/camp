# Proactive use case for CAMP

To build camp go to project root and use:

```bash
docker build . -t camp
```

To run camp within the created image use.

```bash
docker run -it camp bash
```

Work whithin the docker container has some drawbacks. The changes on the current drive are not seem or either presistent. Alternatively, you can also use a mounting point so camp container access an outside folder.


```bash
docker run -t -v $PWD:/campworkingdir camp camp -h
```

Now you can proceed to use camp. For instance for this example change current directory to be `samples/stamp/activeeon` and then run:

```bash
docker run -t -v $PWD:/campworkingdir camp camp generate -d /campworkingdir
```

You can clean exited container and unlinked images using:

```bash
docker system prune
```


## To Do

* Proactive docker container capable of building system tests;
* Add database intial setup;
* Change database configuration for proactive image;
* Run with the 2 selected databases;
* Collect performance measures : memory, cpu, security;
