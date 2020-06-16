---
layout: default
---

# CAMP generate

CAMP generates new configurations given a description of what can be
varied. We use here a simple made-up example to explain how to
generate all configurations, or only the subset that [covers all
possible variations](#coverage), or only [single-change
configurations](#atomic). We then explain how to define
[variables](#variables) and [constraints](#constraints). We also give
a few shell commands to [visualize the generated
configurations](#visualisation).


## CAMP Model

### An "Awesome" Example

We describe here how to use CAMP to vary the testing configurations of
a made-up service called *Awesome*.  This example includes the
following five components:

 1. The component `tests` provides the `Tests` service and requires the
   `Awesome` one. It includes a `threads` variable, whose values are
   range from 10 to 50, and the distance between two
   subsequent sample shall be at most 40.

 2. The `awesome` component is the system under tests. It provides the
   `Awesome` services and requires the `DB` service that both components
   `mysql` and `postgres` provide. To run, it also requires the
   `Python` feature.

 3. The `mysql` component provides the DB service and includes a variable
   to model its two versions, namely v5 and v8.

 4. The `postgres` component also provides the DB services.

 5. The `python` component provides the `Python` feature.


Here is the YAML snippet that captures it:

```yaml
goals:
  running: [ Tests ]

components:
  tests:
    provides_services: [ Tests ]
    requires_services: [ Awesome ]
    variables:
      threads:
        values:
          range: [10, 50]
          coverage: 40
  awesome:
    provides_services: [ Awesome ]
    requires_services: [ DB ]
    requires_features: [ Python ]
  mysql:
    provides_services: [ DB ]
    variables:
      version:
        values: [ v5, v8 ]
  postgres:
    provides_services: [ DB ]
  python:
    provides_features: [ Python ]
```

We can ask CAMP to generate all the possible configurations, as follows:

```bash
$ camp generate -d . --mode all
```

The figure below shows what configurations CAMP generates.

![Awesome configurations]({{site.baseurl}}/assets/images/configurations.png "The six generated configurations")



### Variations Coverage
<a name="coverage"/>

CAMP can enumerate all the possible configurations, but it can also
generate a smaller subset that covers all possible variations at least
one (i.e., components and variable values).

```
$ camp generate --mode coverage -d .
```

In the previous example, CAMP generates only the three following
configurations:

![awesome configurations]({{site.baseurl}}/assets/images/awesome_coverage.png "The
three generated configurations to cover all features")


### Atomic Variations
<a name="atomic"/>

Sometimes we prefer to get configuration that vary from one another by
a single change. CAMP offers the "atomic" mode that does just
that. The first configuration, will be taken as a reference and CAMP
will generate only configuration that differs by single variation
point from this very first configuration.

```
$ camp generate --mode atomic -d .
```


### Features vs. Services

The CAMP model distinguishes between *services* and
*features*. Services are endpoints exposed on the network whereas as
features are capabilities available within the same container.

CAMP only connects component instances when one provides at least one of
the services the other requires. The same hold for features, the
only difference is that a component can only use the feature of a
single component.


### Variables
<a name="variable"/>

CAMP let you defined the variables that may vary in each
component. When CAMP instantiate these components, it will try to find
values for each variable defined in related the component. Variables
may be of several types:

* **Enumerated Variables** are variables whose values are an
  enumeration of symbols. This is often useful to define version as in
  the following example:

  ```yaml
  variables:
	 version:
		values: [ v1, v2, v3.1, v3.2, v4]
  ```

* Numerical Variables are variables whose value is a number (only
  integer are supported so far). There values can be free, constrained
  or enumerated as well.

  * **Free integer variables** are numerical variables that are not
	directly constrained, though constraints may be added separated
	(i.e., in the `constraint` section)

    ```yaml
    variables:
         memory:
          type: Integer
     ```

  * **Enumerated integer variables** are the simples. You basically choose
	what values are legal and CAMP will try to build configuration
	using only those.

    ```yaml
    variables:
         memory:
          type: Integer
          values: [10, 20, 21, 40, 25]
     ```

  * **Range-covering integer variables** are variables whose value is
	taken from a given interval. CAMP uses values spread
	regularly through this interval, as in the example below:

    ```yaml
    variables:
         memory:
          type: Integer
          values:
             range: [10, 30]
             coverage: 5
     ```

	 This declaration forces CAMP to choose a value from [10, 15, 20,
	 25, 30] for the `memory`variable. The *coverage* attribute
	 defines the maximal distance between two subsequent values.


## Constraints
<a name="constraints"/>

You can also add constraints using the [Ozepy
DSL](http://github.com/STAMP-project/ozepy) in order to rule out some
configurations. This is done in the `constraints` section, placed at
the top level, as follows:

```yaml
goals: ...
components: ...
constraints:
    - CInstance.forall(ci.configuration.forall(val, val.value == 0))
```

Here we define a constraint that force all the component instance, to
have 0 as the value for all their variable. We must refer to the [CAMP
metamodel](#metamodel) to write correct constraints.


## Visualization
<a name="visualisation"/>

CAMP also generate [Graphviz](https://www.graphviz.org/)
representation (file named `configuration.dot`) of each configuration
it generates. Provided that graphviz is installed, you can convert a
configuration using:


```bash
$ dot -Tpng configuration.dot -o configuration.png
```

Alternatively, you can convert all configurations using the following
on-liner:

```bash
$ find . -name "*.dot" | xargs -I file dot -Tpng file -o file.png
```

You may also want to gather all these configuration views into a
single picture. Provided
the [imagemagick](https://www.imagemagick.org/) tools are available on
your machine, you can use the following command:

```bash
$ find . -name "*.png" \
   | tr '\n' ' ' \
   | montage  -label '%d/%f' @- -geometry 300x300 configurations.png
```

### The CAMP Metamodel
<a name="metamodel"/>

The figure below illustrates the CAMP model. The green classes will be
generated by the constraint solver, whereas the yellow ones are
specified in the YAML file.

![CAMP metamodel]({{site.baseurl}}/assets/images/camp_metamodel.png "The underlying CAMP metamodel")
