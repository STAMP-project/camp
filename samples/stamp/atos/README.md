# The CityGo Case

I describe here the variation model and the template directory of the
CityGo case. Note that CAMP assumes specific names and structure for
the template directory.


## The Variation Model

The variation model defines the moving parts of the CityGo application
and how they can be logically assembled. These moving parts are named
'components', in the CAMP parlance.

The variation model relies on three key concepts: Services,
Features, and variables. Each component can expose *services*, that
are software interfaces that we can access from another
container. Web servers, databases are often exposed as
"Services". Components can also expose *features*, which represent
interfaces that we can only access from the container where the
component is deployed. Examples of features include libraries,
language framework. Finally, a component may have internal variables,
that are configuration knobs that can have multiple values (either
enumerated or numerical). *Variables* let use model configuration
parameters or versions to name a few.

In a nutshell, *features* let us describe software stack deployed into
a single container, whereas *services* let us describe how to arrange
these stacks into a service orchestration. CAMP relies on services,
features and variables to explore the space of possible assemblies of
of stacks and services.


As for the CityGo case, the variation model specifies the following
components:

  1. The `browser` is the component that contains the tests to be
    run. It requires the `Test` service, that the selenium hub
    provides.
    
  2. The `hub`component represents the selenium hub. It provides the
     `Test` service, and requires the `HttpProxy`service.
  
  3. The `apache` component represents one of the two HTTP proxy
    implementations available, that is one of the two components that
    provides the `HttpProxy`service. It requires the `CityGo` services.
    
  4. The `nginx` component represents the other HTTP proxy available,
     that it also provides the `HttpProxy` service. Besides, this
     component has an internal variable, named `gzip` which can be
     either `true` or `False`. It also requires the `CityGo` service.
  
  5. The `citygo` component represents the `CityGo` application
    running on top of the Django framework. It requires two other
    services, namely the `Postgres` and `Mongo` services. It also
    requires the `Python` feature.
    
  6. The `python` component represents the Python interpreter on top
    of which Django executes. It provides the `Python` feature that
    the `citygo` component requires, but it requires in turn the
    `Ubuntu` feature.
    
  7. The `mongo`component represents the MongoDB instance that CityGo
    requires. It provides the `Mongo` service.
    
  8. The `postgres` component represents the PostgreSQL instance that
    CityGO requires. It provides the `Postgres` service.
    
  9. The `ubuntu`component simply provides the `Ubuntu` features,
     needed by the `python` component.
  

This model yields three configurations, as shown in the figure below.

![The three configuration of the CityGo case](configurations.png)

These three configurations result from two variation points: The first
one is the `gzip` variable of the `nginx` component, which is either
"True" or "False". The second one, is the existence of two alternative
components that both provide the `HttpProxy` service.

---

**Note 1** The variation model *does NOT* have to state every single
component of your application if some are not involved in variation
you want CAMP to generate. We must only specifies when:
 1. CAMP must assemble the piece in mutliple ways in order to explore
    alternatives configuration that we want to test
 1. CAMP must configure the pieces in different ways, for instance by
modifying some local configuration files.
 1. CAMP must trigger a command onto the pieces to run the tests
template.

We can often "hardcode" other pieces that are not involved
in variations, into the service orchestration.

---


## The Template

CAMP copies and then modifies this template directory to obtain each
configuration it finds.

The template directory makes explicit the operational details for each
moving part, except the parts that are directly implemented by a
docker image, such as the `hub`.

CAMP expect to find the docker-compose files at the root of the
template directory, so the layout must be similar to :

```console
$ tree template -L 2
template
├── apache
│   ├── demo_site.conf
│   ├── Dockerfile
│   └── mpm_event.conf
├── browser
│   ├── Dockerfile
│   └── tests.py
├── citygo
│   └── Dockerfile
├── docker-compose-apache-as-proxy.yml
├── docker-compose-apache.yml
├── docker-compose-nginx.yml
├── nginx
│   ├── Dockerfile
│   └── nginx.tmpl
├── postgres
│   ├── Dockerfile
│   ├── init-db.sql
│   └── postgresql.conf
└── python
    └── Dockerfile
```


### `template/apache`

This directory contains the material needed for Docker to install the
`apache` component we have listed in the variation model.  This is a
regular Dockerfile has we have not split the underlying stack into multiple
components (See Note 1).


### `template/browser`

This directory contains the sources (Python files) of the tests to be
run, as well as a Dockerfile to install these tests. As we specified in
the `camp.yml` model, CAMP will connect to the associated container and
will trigger `pytest`to run the tests (see the excerpt of the variation
model below).

```yaml
    tests:
      command: pytest -v tests.py --junitxml=report.xml
      reports:
        location: "./"
        pattern: ".xml"
        format: junit
```

CAMP will then look for the test reports in this container and
aggregate the results it finds there.


### `template/citygo`

This directory should contain the material needed to install CityGo
application. In principle, as we have split the underlying stack into
three component, we cannot assume any base image and the FROM
statement will be computed by CAMP. However, in this very case, the
stack is always the same in all three configurations, so we can assume
we deploy on top of the `python` component (see `template/pyhton`).


### `template/nginx`

This directory contains the material needed for Docker to install the
`nginx` component we have listed in the variation model. This is a
regular Dockerfile has we have not split the underlying stack into
multiple components (See Note 1).


### `template/postgres`

Contains the material needed to install the `postgres` component. This
is a regular Dockerfile as we have not broken down the underlying
stack into separate components (See Note 1).

### `template/python`

Here we explain in a Dockerfile how to install the `python` component
we have listed in the `camp.yml` directory. Note that we cannot assume
any base image, and the FROM statement will therefore be computed by
CAMP, during the realisation. However, all the configurations that our
model yield have the Python component deployed on top the `ubuntu`
component.

