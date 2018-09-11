# CAMP-Exe for docker-compose
The modules allows to exactute docker-compose files and experiments required to asses a given configuration of the software defined in a docker-compose file.

## How to use
### Testing
To execute test cases, run the following command:
```
> tox -e py27local
```
Some test cases actually executes scripts and docker-compose up/down commands. You can find those test cases in tests/test_e2e.py. To skip execution of these test, please run the following command:
```
$ tox -e py27local -- tests.test_simple_units:TestSimpleUnits
```
### Installation
```
$ sudo python setup.py install
```

### Usage
To run the tool, you need to exectue:
```
$ campexe docker-compose <path_to_configuration_file>
```

### Examples
To run the example, please go to camp/modules/camp-exe-docker-comp and execute the following command:
```
$ campexe docker-compose examples/simple/config.ini
```
In this example, CAMP-exe deploys a simple web application, makes a request to the application and kills the application. The output should look as follows:
```
Executing: ./setup_composetest.sh param1 at examples/simple/scripts
setup! param1
Executing: docker-compose up -d at examples/simple/composetest
Creating network "composetest_default" with the default driver
Creating composetest_redis_1 ... done
Creating composetest_web_1   ... done
Executing: ./exp_composetest.sh param1 param2 at examples/simple/scripts
Waiting for 5 sec to set up deployment
Hello World! I have been called. param1:param1 param2:param2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    33  100    33    0     0   3051      0 --:--:-- --:--:-- --:--:--  3300
Executing: docker-compose down at examples/simple/composetest
Stopping composetest_web_1   ... done
Stopping composetest_redis_1 ... done
Removing composetest_web_1   ... done
Removing composetest_redis_1 ... done
Removing network composetest_default
Executing: ./teardown_composetest.sh param1 at examples/simple/scripts
teardown! param1
Completed!

```

A single execution of CAMP-exe is guided by a configuration file. An execution of CAMP-exe can be thought of as a unit test case for the deployment described in a docker-compose file. The configuration file defines a set of scripts to set up, tear down a test experiment, deploy the application, and execute the experiment on the deployed application. The content of the configuration file may look as follows:
```
[pre_post]
setup = examples/simple/scripts/setup_composetest.sh
setup_params = param1
teardown = examples/simple/scripts/teardown_composetest.sh
teardown_params = param1

[docker_compose]
compose_files = examples/simple/composetest/docker-compose.yml

[experiment]
script = examples/simple/scripts/exp_composetest.sh
params = param1 param2
```
The configuration file consiste of three sections, i.e. ```[pre_post]```, ```[docker_compose]```, ```[experiment]```.

The ```[pre_post]``` section contains paths to setup and tear down scripts along with the parameters for these scripts. The parameters is a string seperated by whitespaces. The string is parsed and fed into a command line as arguments for a corresponding script, e.g. a ```setup_params``` string is fed into a ```setup``` script.

The ```[experiment]``` section references a script to perform an experiment on a running systems which is spawn off with help of docker-compose. The experiment can be thought of as a test to check properties of the running system. This section also has the ```params``` field with paramers to feed into the experiment script. The ```params``` field contains a string with parameters seperated by whitespaces.

The ```[docker_compose]``` has the ```compose_files``` field with a list of docker-compose files seperated by semicolons. CAMP-exe executes setup, tear down and experiment script for each docker-compose files.
