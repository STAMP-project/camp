# CAMP-exe for docker compose
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
### Usage

### Examples
