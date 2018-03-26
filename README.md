[![Build Status](https://travis-ci.org/SINTEF-9012/camp-realize.svg?branch=master)](https://travis-ci.org/SINTEF-9012/camp-realize)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce234e0552f34484abf4ce89360c5b8a)](https://www.codacy.com/app/vassik/camp-realize?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SINTEF-9012/camp-realize&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/SINTEF-9012/camp-realize/branch/master/graph/badge.svg)](https://codecov.io/gh/SINTEF-9012/camp-realize)

# CAMP-realize
CAMP-realize is a standalone tool to perform arbitrary modifications of any given artifact to yield a new artifact which is different from the given one. The tool is used in conjunction with [CAMP](https://github.com/STAMP-project/camp) to modify variables (variation points) in configuration files.

## How to use
### Testing
To execute test cases, run the following command:
```
> tox -e py27local
```

### Installation
To install from the source code:
```
> python setup.py install
```
The tool is not yet available in any public repository and therefore could be installed using pip

### Execution
The following command generates new artifacts by modifying existing artifacts given in a product model, i.e. realizes the product model.
``` 
> cd examples/ && rcamp realize examples/product_model.yaml
```
## Models
### Product model
A product model contains a description of products to realize. Each description for the product contains: name, product path, path to a realization model, variables to realize. Example:
```
products:
  - product1:
      product_dir: "tests/resources/simple_e2e_regexp/tmp/product1/"
      realization:
        path: "tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml"
        variables:
          - variable1: value1
          - variable2: value1
```
1. ```product_dir``` contains a path to product artifacts(the path is relative to the directory where we run the tool).
2. ```path``` contains a path to a realization model (the path is relative to the directory where we run the tool, i.e. examples). The realization model contains definitions to variables and values defined in the variables section.
3. ```variables``` contains two variables, i.e. ```variable1```, ```variable2``` which should be resolved to ```value1```.

### Realization model
A realization model contains a list of variables with their values. In addition, it defines how variables and values should be materialized. Example:
```
variable1:
    value1:
        type: int
        value: 10
        operations:
            - substituion1:
                engine: regexp
                filename: "images/Dockerfile"
                placement: "jenkins:latest"
                replacement: "jenkins:lts"
variable2:
    value1:
        operations:
            - substituion1:
                engine: regexp
                filename: "images/Dockerfile"
                placement: "USER jenkins"
                replacement: ""
```
The realization model contains definition of two variables, and operations which the tool needs to execute to materialize the variables. For example:
1. ```variable2``` is a name of the variable with only one possible value, i.e. ```value1```.
2. ```operations``` contains a list of operations to execute, i.e. one operation with name ```substitution1```.
3. ```substitution1``` - a regexp operation which substitutes the placement "USER jenkins" with an empty string in the file "images/Dockerfile"
4. ```filename``` is a path to the file which is relative to a product directory
