---
layout: default
---

# How to install CAMP?

CAMP is a [Python 3.7](https://www.python.org/) application, which
uses the [Z3 theorem prover](https://github.com/Z3Prover/z3) behind
the scenes. These are therefore the two mandatory dependencies that
must installed on your machine.

You can install CAMP in three main ways:

2.  [Using Docker](#using-docker) (recommended) ;
1.  [Using our install script](#from-internet) ;
3.  [Manually](#manually).

If these do not work, check out the [troubleshooting
section](#troubleshooting) on possible issues and resolution.



<a name="using-docker" />
## Installing using Docker

The fastest solution is to use [docker](https://www.docker.com/) to
run CAMP and all its dependencies in one container, using the
following command:

```console
fchauvel@debian$ docker run --name camp \
             -it \
             -v /var/run/docker.sock:/var/run/docker.sock \
             -t fchauvel/camp:latest bash
root@9dd7e1f061ce:/camp# cd samples/java
root@9dd7e1f061ce:/camp# camp generate -d .
```

As shown above, the CAMP image already contains the code source and
the examples in the `samples` directory.

Note that we share the docker deamons of the host with the CAMP
container (see the `-v /var/run/docker.sock:...` option). CAMP can
therefore invoke docker and create "siblings" containers.

This command will fetch the CAMP Docker image named
`fchauvel/camp:latest` from [Docker
Hub](https://hub.docker.com/r/fchauvel/camp/) and run it with your
working directory ($pwd) mounted in the container at `/workspace`.

We follow the following convention for tags on our Docker images:

 * `vX.Y.Z` define the version of CAMP that is running
 * `latest` define the latest released of CAMP (i.e., the higgest
   version vX.Y.Z)
 * `dev` define the latest commit that passed the CI checks.


<a name="from-internet"/>
## Using the Install Script

Another way is to use our install script, which you can fetch and
execute as follows:

```bash
$ \curl -L https://github.com/STAMP-project/camp/raw/master/install.sh \
  | sudo bash -s -- --install-z3 --z3-python-bindings /usr/lib/python3.7
```

This script installs both the Z3 solver and CAMP. It accepts the
following arguuments:

```console
Usage: sh install.sh [options...]
Options:
  -c, --camp-version STRING     Select a specific version of CAMP from Github.
                                Can be a branch name (e.g., 'master'), a tag, or
                                a commit hash. Default is 'master'.
  -d, --install-docker          Install Docker.io (CE version). By default,
                                Docker will not be installed.
  -l, --z3-platform STRING      Install Z3 for a specific version of linux.
                                Default is 'x64-debian-8.10'.
  -g, --debug                   Debugging mode: display all commands and log
                                output in a file. Disabled by default.
  -i, --install-z3              Install Z3 if not already available. By default,
                                Z3 will notbe installed.
  -p, --z3-python-bindings DIR  Set the installation directory for the Z3 Python
                                bindings. Default is '/usr/lib/python3.7'.
  -s, --camp-from-sources       Install CAMP for sources expected to be in
                                the working directory. By default, CAMP is
                                downloaded from Github.
  -t, --camp-with-tests         Install CAMP with its test dependencies. By 
                                default, these are not installed.
  -z, --z3-version STRING       Set the version of the Z3 solver to install.
                                Default is '4.7.1'.
```

Here, we specified where the Z3 Python bindings must be installed.

Note the `--camp-version`, which let you install a specific version of
CAMP. Here, we installed the development version, directly from the
`master` branch.

Once it completed, you can check that CAMP is running as follows:

```console
$ camp --help
usage: CAMP [-h] {generate,realize,execute} ...

Amplify your configuration tests!

positional arguments:
  {generate,realize,execute}
    generate            Generate new test configurations
    realize             Realize the variables in the test configurations
    execute             Execute the test configurations generated

optional arguments:
  -h, --help            show this help message and exit
```



<a name="manually" />
## Installing from Scratch

### Installing Python 3.7

Python 3.7 is installed on many Linux distribution. Should you need to
install it yourself, please follow the instruction given on the
[Python website](https://www.python.org/) for your environment.


### Installing Z3 Solver


First, download and unzip the last version of the Z3 solver from the
[GitHub releases](https://github.com/Z3Prover/z3/releases/). At the
time of writing, the last version is Z3 4.7.1. Then, unzip the archive
that fits your platform in a directory of your choice, I use
`unzipped` in the following.

```bash
$ cd /root
$ wget https://github.com/Z3Prover/z3/releases/download/z3-4.7.1/z3-4.7.1-x64-debian-8.10.zip
$ unzip z3-4.7.1-x64-debian-8.10.zip && mv z3-4.7.1-x64-debian-8.10 unzipped
```

Now, create the directory that will contain the Z3 binaries. I install
it within the Python 3.7 distribution in `/usr/lib/python3.7`, and copy
the relevant executable file, the Z3 libraries, and the Z3 Python
bindings.

```bash
$ mkdir -p /usr/lib/python3.7/z3/lib
$ cp unzipped/bin/z3 /usr/lib/python3.7/z3/lib/
$ cp unzipped/bin/lib* /usr/lib/python3.7/z3/lib/
$ cp -rf unzipped/bin/python/z3 /usr/lib/python3.7/
$ ln -s /usr/lib/python3.7/z3/lib/z3 /usr/bin/z3
$ rm -rf unzipped

```

You can now check that Z3 is available, by checking its version number
as follows:

```console
$ z3 --version
Z3 version 4.7.1 - 64 bit
```

You can also check the Z3 Python bindings are properly set up by
executing this Python one-liner:

```console
$ python -c 'import z3; print(z3.get_version_string())'
4.7.1
```


> **NOTE for CAMP contributors** If you are installing CAMP in order
> to modify it, you may want to create virtual environments that include
> the Z3 bindings we just installed globally. To do so use
> `--system-site-packages` option when you create your virtual
> environment, as follows:
>
> ```console
> $ virtualenv -p /usr/bin/python3.7 --system-site-package .venv3.7
> $ source .venv3.7/bin/activate
> (.venv3.7) $ python -c 'import z3; print(z3.get_version_string())'
> 4.7.1
> ```


### Installing CAMP

As for most of Python applications, the simplest way to install it is
using PIP as follows:

```bash
$ pip install -U https://github.com/STAMP-project/camp.git@master#egg=camp
```

You can check the installation be running:

```console
$ camp version
1.0.0
```


> **NOTE for CAMP contributors** To install CAMP in a development
> mode, use the `-e` flag so that your changes get picked up
> automatically.
>
> ```console
> $ git clone https://github.com/stamp-project/camp.git
> $ cd camp
> $ pip install -e .
> $ camp version
> 1.0.0
> ```


<a name="troubleshooting" />
## Troubleshooting

### If the Z3 Python bindings cannot find `libz3.so`

Depending on the Z3 version you are running, the Z3 Python bindings
may not be able to find the Z3 library, though it is properly
installed. On Debian Jessie, we saw this when testing the Python
bindings as follows:

```console
$ python -c "from z3 import *"
Could not find libz3.so; consider adding the directory containing it to
  - your system's PATH environment variable,
  - the Z3_LIBRARY_PATH environment variable, or
  - to the custom Z3_LIBRARY_DIRS Python-builtin before importing the z3 module, e.g. via
	import __builtin__
	__builtin__.Z3_LIB_DIRS = [ '/path/to/libz3.so' ]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python3.7/z3/__init__.py", line 1, in <module>
	from .z3 import *
  File "/usr/lib/python3.7/z3/z3.py", line 44, in <module>
	from . import z3core
  File "/usr/lib/python3.7/z3/z3core.py", line 64, in <module>
	raise Z3Exception("libz3.%s not found." % _ext)
z3.z3types.Z3Exception: libz3.so not found.
```

We found this message very misleading as setting these environment
variables did not help. Eventually, a more relevant error message is
returned by Z3 itself when we tried to run it from the command line:

```console
$ z3 --version
z3: error while loading shared libraries: libgomp.so.1: cannot open shared object file: No such file or directory

```

**FIX** Installing this library seems to be a prerequisite. It eventually solved the problem:
```bash
$ apt-get install libgomp1
```
