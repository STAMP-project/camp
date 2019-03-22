#!/bin/bash -f

set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace


# Check if curl is available
if ! type curl >/dev/null 2>&1; then
    echo "Error: curl is needed by not available";
    echo "You may want to install curl using: 'apt-get install curl";
    exit 1;
fi

# Check if git is available
if ! type git >/dev/null 2>&1; then
    echo "Git is required, but not available.";
    echo "You may want to install git using: 'apt-get install git";
    exit 1;
fi

# Check if PIP is available
PIP_VERSION=19.0.3
if ! type pip >/dev/null 2>&1; then
    echo "PIP is not available, installing Version ${PIP_VERSION}";
    \curl -sS -L -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
    python get-pip.py -q pip==$PIP_VERSION;
    rm get-pip.py

else
    echo "Upgrading PIP ..."
    pip -q install --upgrade pip==$PIP_VERSION
fi

# Install Z3 if not already available
if ! type z3 >/dev/null 2>&1; then
    Z3_VERSION=${Z3_VERSION:-z3-4.7.1}
    Z3_PLATFORM=${Z3_PLATFORM:-x64-debian-8.10}

    Z3_ARCHIVE=$Z3_VERSION-$Z3_PLATFORM.zip
    Z3_ARCHIVE_URL=https://github.com/Z3Prover/z3/releases/download/$Z3_VERSION/$Z3_ARCHIVE
    Z3_DIRECTORY=$(basename -s .zip $Z3_ARCHIVE)

    PYTHON_LIB_PATH=/usr/lib/python2.7

    if ! [ -f $Z3_ARCHIVE ]; then
        \curl -sS -L -O $Z3_ARCHIVE_URL
    fi

    unzip -q $Z3_ARCHIVE
    mkdir -p $PYTHON_LIB_PATH/z3/lib
    cp $Z3_DIRECTORY/bin/z3 $PYTHON_LIB_PATH/z3/lib/
    cp $Z3_DIRECTORY/bin/lib* $PYTHON_LIB_PATH/z3/lib/
    cp -rf $Z3_DIRECTORY/bin/python/z3 $PYTHON_LIB_PATH
    ln -s $PYTHON_LIB_PATH/z3/lib/z3 /usr/bin/z3
    rm -rf $Z3_DIRECTORY
    #rm -rf $Z3_ARCHIVE

    if z3 --version >/dev/null 2>&1; then
        echo "Z3 ready."
    else
        echo "Error: Z3 not still not available.";
        echo "Aborting.";
        exit 1;
    fi

    python -c 'import z3; print(z3.get_version_string())' >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Z3 Python bindings ready."
    else
        echo "Error: Z3 Bindings are not available.";
        echo "Is '${PYTHON_LIB_PATH}' the path to the Python's libraries?"
        echo "Aborting.";
        exit 1;
    fi

fi


# Installing CAMP
CAMP_VERSION=${CAMP_VERSION:-master}
CAMP_URL=https://github.com/STAMP-project/camp.git@${CAMP_VERSION}#egg=camp
LOG_FILE=camp_install.log

pip --log=${LOG_FILE} install git+${CAMP_URL}
if [ $? -eq 0 ]; then
    echo "CAMP (${CAMP_VERSION}) ready.";
else
    echo "Error. (See logs in ${LOG_FILE})"
fi
