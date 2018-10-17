---
layout: default
---

# CAMP Realize

CAMP-realize is a standalone tool to perform arbitrary modifications
of any given artifact to yield a new artifact which is different from
the given one. The tool is used in conjunction with
[CAMP](https://github.com/STAMP-project/camp) to modify variables
(variation points) in configuration files.

# Usage

The following command generates new artifacts by modifying existing
artifacts given in a product model, i.e. realizes the product model.

```bash
$> camp realize -p product_model.yaml
```

## Product Model

A product model contains a description of products to realize. Each
description for the product contains: name, product path, path to a
realization model, variables to realize. Example:

```yaml
products:
  - product1:
      product_dir: "tests/resources/simple_e2e_regexp/tmp/product1/"
      realization:
        path: "tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml"
        variables:
          - variable1: value1
          - variable2: value1
```

1. `product_dir` contains a path to product artifacts, i.e., product
   directory.

2. `path` contains a path to a realization model. The realization
   model contains definitions to variables and values defined in the
   variables section.

3. `variables` contains two variables, i.e. `variable1`, `variable2`
   which should be resolved to `value1`.


## Realization Model

A realization model contains a list of variables with their values. In
addition, it defines how variables and values should be
materialized. Example:

```yaml
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

The realization model contains definition of two variables, and
operations which the tool needs to execute to materialize the
variables. For example:

1. `variable2` is a name of the variable with only one possible value,
   i.e., `value1`.

2. `operations` contains a list of operations to execute, i.e. one
   operation with name `substitution1`

3. `substitution1` - a regexp operation which substitutes the
   placement "USER jenkins" with an empty string in the file
   "images/Dockerfile"

4. `filename` is a path to the file which is relative to a product
   directory
