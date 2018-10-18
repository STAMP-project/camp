---
layout: default
---

# How to install CAMP?

CAMP is a [Python 2.7](https://www.python.org/) application, which
uses the [Z3 theorem prover](https://github.com/Z3Prover/z3) behind
the scenes. These are therefore the two mandatory dependencies that
must installed on your machine.


## Installing using Git & Docker

The simplest solution is to use [docker](https://www.docker.com/) to
run CAMP and all its dependencies in one container, using the
following command:

```bash
docker run -it -v $(pwd):/camp/workspace fchauvel/camp:v1.0.0 camp generate -d workspace
``` 

This command will fetch the CAMP Docker image named
`fchauvel/camp:v1.0.0` from [Docker
Hub](https://hub.docker.com/r/fchauvel/camp/) and run it with your
working directory ($pwd) mounted in the container at `/workspace`.

We follow the following convention for tags on our Docker images:

 * `vX.Y.Z` define the version of CAMP that is running
 * `latest` define the latest released of CAMP (i.e., the higgest
   version vX.Y.Z)
 * `dev` define the latest commit that passed the CI checks.



## Installing from Scratch

### Installing Python 2.7

Python 2.7 is installed on many Linux distribution. Should you need to
install it yourself, please follow the instruction given on the
[Python website](https://www.python.org/) for your environment.


### Installing Z3 Solver


First, download and unzip the last version of the Z3 solver from the
[GitHub releases](https://github.com/Z3Prover/z3/releases/). At the
time of writing, the last version is Z3 4.7.1. Then, unzip the archive
that fits your platform in a directory of your choice, I use
`unzipped` in the following.

```bash
$> cd /root
$> wget https://github.com/Z3Prover/z3/releases/download/z3-4.7.1/z3-4.7.1-x64-debian-8.10.zip
$> unzip z3-4.7.1-x64-debian-8.10.zip && mv z3-4.7.1-x64-debian-8.10 unzipped 
```

Now, create the directory that will contain the Z3 binaries. I install
it within the Python2.7 distribution in `/usr/lib/python2.7`, and copy
the relevant executable file, the Z3 libraries, and the Z3 Python
bindings.

```bash
$> mkdir -p /usr/lib/python2.7/z3/lib
$> cp unzipped/bin/z3 /usr/lib/python2.7/z3/lib/ 
$> cp unzipped/bin/lib* /usr/lib/python2.7/z3/lib/
$> cp -rf unzipped/bin/python/z3 /usr/lib/python2.7/ 
$> ln -s /usr/lib/python2.7/z3/lib/z3 /usr/bin/z3
$> rm -rf unzipped

```

You can now check that Z3 is available, by checking its version number
as follows:

```bash
$> z3 --version
Z3 version 4.7.1 - 64 bit
```

You can also check the Z3 Python bindings are properly set up by
executing this Python one-liner:

```bash
$>  python -c 'import z3; print(z3.get_version_string())'
4.7.1
```

--- 
**NOTE for CAMP contributors** If you are installing CAMP in order
to modify it, you may want to create virtual environments that include
the Z3 bindings we just installed globally. To do so use
`--system-site-packages` option when you create your virtual
environment, as follows:

```bash
$> virtualenv -p /usr/bin/python2.7 --system-site-package .venv2.7 
$> source .venv2.7/bin/activate
(.venv2.7) $> python -c 'import z3; print(z3.get_version_string())'
4.7.1
```
---

### Installing CAMP

As for most of Python applications, the simplest way to install it is
using PIP as follows:

```bash
$> pip install https://github.com/stamp-project/camp.git@master#egg=pip
```

You can check the installation be running:

```bash
$> camp version
1.0.0
```

--- 
**NOTE for CAMP contributors** To install CAMP in a development
mode, use the `-e` flag so that your changes get picked up
automatically.

```bash
$> git clone https://github.com/stamp-project/camp.git
$> cd camp
$> pip install -r requirements.txt
$> pip install -e .
$> camp version
1.0.0
```
---

## Troubleshooting

### If the Z3 Python bindings cannot find `libz3.so`

Depending on the Z3 version you are running, the Z3 Python bindings
may not be able to find the Z3 library, though it is properly
installed. On Debian Jessie, we saw this when testing the Python
bindings as follows:

```bash
$> python -c "from z3 import *"
Could not find libz3.so; consider adding the directory containing it to
  - your system's PATH environment variable,
  - the Z3_LIBRARY_PATH environment variable, or 
  - to the custom Z3_LIBRARY_DIRS Python-builtin before importing the z3 module, e.g. via
    import __builtin__
    __builtin__.Z3_LIB_DIRS = [ '/path/to/libz3.so' ] 
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python2.7/z3/__init__.py", line 1, in <module>
    from .z3 import *
  File "/usr/lib/python2.7/z3/z3.py", line 44, in <module>
    from . import z3core
  File "/usr/lib/python2.7/z3/z3core.py", line 64, in <module>
    raise Z3Exception("libz3.%s not found." % _ext)
z3.z3types.Z3Exception: libz3.so not found.
```

We found this message very misleading as setting these environment
variables did not help. Eventually, a more relevant error message is
returned by Z3 itself when we tried to run it from the command line:

```bash
$> z3 --version
z3: error while loading shared libraries: libgomp.so.1: cannot open shared object file: No such file or directory

```

**FIX** Installing this library seems to be a prerequisite. It eventually solved the problem:
```bash
$> apt-get install libgomp1
```
