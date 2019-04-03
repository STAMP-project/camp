#!/usr/bin/env sh

set -o errexit
set -o errtrace
set -o pipefail
set -o nounset

DEBUG=false
LOG_FILE=install.log

# Default parameters values

PYTHON_VERSION=3.5
Z3_VERSION=4.7.1
Z3_PLATFORM=x64-debian-8.10
Z3_BINDINGS=/usr/lib/python${PYTHON_VERSION}
INSTALL_PYTHON=false
INSTALL_Z3=false
INSTALL_DOCKER=false
CAMP_VERSION=master
CAMP_FROM_SOURCES=false
CAMP_WITH_TESTS=


USAGE=$(IFS='' cat <<'EOF'
Usage: sh install.sh [options...]
Options:
  -d, --install-docker          Install Docker.io (CE version). By default,
                                Docker will not be installed.
  -y, --install-python          Install Python. Disabled by default.
  -h, --python-version STRING   Select a specific version of Python to be 
                                installed. Set to 3.5 by default.
  -i, --install-z3              Install Z3 if not already available. By default,
                                Z3 will notbe installed.
  -p, --z3-python-bindings DIR  Set the installation directory for the Z3 Python
                                bindings. Default is '/usr/lib/python3.5'.
  -z, --z3-version STRING       Set the version of the Z3 solver to install.
                                Default is '4.7.1'.
  -l, --z3-platform STRING      Install Z3 for a specific version of linux.
                                Default is 'x64-debian-8.10'.
  -c, --camp-version STRING     Select a specific version of CAMP from Github.
                                Can be a branch name (e.g., 'master'), a tag, or
                                a commit hash. Default is 'master'.
  -s, --camp-from-sources       Install CAMP for sources expected to be in
                                the working directory. By default, CAMP is
                                downloaded from Github.
  -t, --camp-with-tests         Install CAMP with its test dependencies. By 
                                default, these are not installed.
  -g, --debug                   Debugging mode: display all commands and log
                                output in a file. Disabled by default.
EOF
);



abort () {
    printf "Aborting!\n"
    tail --lines 30 ${LOG_FILE}
}



parse_arguments () {
    while [ $# -gt 0 ]; do
        case "$1" in
            -d|--install-docker)
                INSTALL_DOCKER=true
                shift 1
                ;;
            -y|--install-python)
                INSTALL_PYTHON=true
                shift 1
                ;;
            -h|--python-version)
                PYTHON_VERSION="$2"
                shift 2
                ;;
            -i|--install-z3)
                INSTALL_Z3=true
                shift 1
                ;;
            -z|--z3-version)
                Z3_VERSION=$2
                shift 2
                ;;
            -l|--z3-platform)
                Z3_PLATFORM="$2"
                shift 2
                ;;
            -p|--z3-python-bindings)
                Z3_BINDINGS="$2"
                shift 2
                ;;
            -c|--camp-version)
                CAMP_VERSION="$2"
                shift 2
                ;;
            -s|--camp-from-sources)
                CAMP_FROM_SOURCES=true
                shift 1
                ;;
            -t|--camp-with-tests)
                CAMP_WITH_TESTS=[test]
                shift 1
                ;;
            -g|--debug)
                DEBUG=true
                shift 1
                ;;
            *)
                printf "Error: Unknown option '$1'.\n"
                printf "${USAGE}\n"
                exit 1
        esac
    done
}



install_packages () {
    apt-get install -y --no-install-recommends $* >> ${LOG_FILE} 2>&1
}



version_of () {
    local -r tool=$1
    local -r flag=${2:-"--version"}
    local -r regex="[0-9]+(\.[0-9]+)+"
    local -r version=$($tool $flag | grep -Eo ${regex} | head -1)
    printf "%s\n" "$version"
}



ensure_python_available () {
    if [[ "${INSTALL_PYTHON}" == "true" ]] && ! type python >> ${LOG_FILE} 2>&1
    then
        printf "Installing Python %s ...\n" "${PYTHON_VERSION}"
        # The package 'pythonX-minimal does not contains the module
        # 'shutil' which is required by the 'getpip.py' script.
        install_packages python${PYTHON_VERSION} python-pkg-resources
        rm -rf  /usr/bin/python
        ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python 
    fi
}



ensure_curl_available() {
    if ! type curl >> ${LOG_FILE} 2>&1;
    then
        printf "Installing curl ...\n"
        install_packages ca-certificates curl
    fi
}



ensure_git_available() {
    if ! type git >> ${LOG_FILE} 2>&1;
    then
        printf "Installing git ...\n"
        install_packages git
    fi
}


ensure_libgomp_available () {
    if ! /sbin/ldconfig -p | grep libgomp >> ${LOG_FILE} 2>&1;
    then
        printf "Installing libgomp ...\n"
        install_packages libstdc++6 libgomp1
    fi
}



ensure_unzip_available() {
    if ! type unzip >> ${LOG_FILE} 2>&1;
    then
        printf "Installing unzip ...\n"
        install_packages unzip
    fi
}



ensure_docker_available () {
    if [[ "${INSTALL_DOCKER}" == "true" ]] && ! type docker >> ${LOG_FILE} 2>&1;
    then
        printf "Installing Docker ... (be patient)\n"
        install_packages \
                apt-transport-https \
                ca-certificates \
                curl \
                gnupg2 \
                software-properties-common
        curl -fsSL https://download.docker.com/linux/debian/gpg \
            | apt-key add - >> ${LOG_FILE} 2>&1
        add-apt-repository \
             "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
        apt-get -qq update
        install_packages docker-ce-cli

        #Installing Docker Compose
        curl -fsSL https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
}



compare_version() {
    local -r left=($(echo $1 | tr -s '.' ' '))
    local -r right=($(echo $2 | tr -s '.' ' '))
    local -r max_length=$((${#left[@]} > ${#right[@]} ? ${#left[@]} : ${#right[@]}))
    local result='=='
    for i in $(seq 0 $((max_length - 1)));
    do
        local left_number=${left[i]:-0}
        local right_number=${right[i]:-0}
        if [ "${left_number}" -eq "${right_number}" ];
        then
            continue
        fi
        if [ "${left_number}" -gt "${right_number}" ];
        then
            result='>'
            break
        else
            result='<'
            break
        fi
    done
    printf "%s\n" ${result}
}


ensure_pip_available() {
    local -r PIP_VERSION="19.0.3"
    if ! type pip >> ${LOG_FILE} 2>&1;
    then
        ensure_curl_available
        printf "Installing Pip ${PIP_VERSION}.\n";
        local -r PIP_INSTALLER_URL=https://bootstrap.pypa.io/get-pip.py
        \curl -sS -L -k -O ${PIP_INSTALLER_URL};
        python get-pip.py -qq pip==$PIP_VERSION;
        rm get-pip.py

    else
        local PIP="pip"
        #if [[ "${PYTHON_VERSION}" =~ "^2" ]]
        #then
        #   PIP="pip2"
        #fi
        local -r current_version=$(version_of "pip")
        printf ">>>%s<<<\n" $current_version
        comparison=$(compare_version ${current_version} ${PIP_VERSION})
        if [ "$comparison" == "<" ]
        then
            printf "Upgrading Pip from %s to %s\n" ${current_version} ${PIP_VERSION}
            ${PIP} -qq install --upgrade pip==$PIP_VERSION
        fi
    fi
}


test_Z3() {
    local -r TEST_Z3="z3 --version"
    if ${TEST_Z3} >> ${LOG_FILE} 2>&1
    then
        printf "Z3 %s ready.\n" ${Z3_VERSION}
    else
        printf "Error: Z3 not working!\n";
        abort
    fi
}


test_Z3_python_bindings() {
    ensure_python_available
    local -r TEST_BINDINGS="/usr/bin/python -c \"import z3; print(z3.get_version_string())\""
    if eval "${TEST_BINDINGS}" >> ${LOG_FILE} 2>&1
    then
        printf "Z3 Python bindings ready. (%s)\n" ${Z3_BINDINGS}
    else
        printf "Error: Z3 Bindings not working!\n";
        printf "Is '%s' the path to the Python's libraries?\n" ${Z3_BINDINGS}
        abort
    fi
}



ensure_Z3_available() {
    if [[ "${INSTALL_Z3}" == "true" ]] && ! type z3 >> ${LOG_FILE} 2>&1; then
        printf "Installing Z3 %s for (%s) ...\n" ${Z3_VERSION} ${Z3_PLATFORM}
        ensure_python_available
        ensure_libgomp_available
        ensure_curl_available
        ensure_unzip_available
        local -r Z3_VERSION_NUMBER=$(echo ${Z3_VERSION} | grep -Eo "([0-9]+\.[0-9]+\.[0-9]+)") 
        local -r Z3_ARCHIVE=z3-${Z3_VERSION}-${Z3_PLATFORM}.zip
        local -r Z3_URL="https://github.com/Z3Prover/z3/releases/download/z3-%s/%s"
        local -r Z3_ARCHIVE_URL=$(printf $Z3_URL $Z3_VERSION_NUMBER $Z3_ARCHIVE)
        local -r Z3_DIRECTORY=$(basename -s .zip $Z3_ARCHIVE)

        if ! [ -f ${Z3_ARCHIVE} ]; then
            \curl -sS -L -O ${Z3_ARCHIVE_URL}
        fi

        \unzip -q ${Z3_ARCHIVE}
        \mkdir --parents ${Z3_BINDINGS}/z3/lib
        \cp ${Z3_DIRECTORY}/bin/z3 ${Z3_BINDINGS}/z3/lib/
        \cp ${Z3_DIRECTORY}/bin/libz3.so ${Z3_BINDINGS}/z3/lib/
        \cp -rf ${Z3_DIRECTORY}/bin/python/z3 ${Z3_BINDINGS}
        \ln -s ${Z3_BINDINGS}/z3/lib/z3 /usr/bin/z3
        \rm -rf ${Z3_DIRECTORY}
        \rm -rf ${Z3_ARCHIVE}

        test_Z3
        test_Z3_python_bindings
    fi
}


ensure_CAMP_available() {
    ensure_python_available
    ensure_git_available
    ensure_pip_available
    ensure_Z3_available
    ensure_docker_available


    if [[ "${CAMP_FROM_SOURCES}" == "true" ]]
    then
        pip install --upgrade setuptools >> ${LOG_FILE} 2>&1
        pip install .${CAMP_WITH_TESTS} >> ${LOG_FILE} 2>&1

    else
        local -r GITHUB_URL="https://github.com/STAMP-project/camp.git@%s#egg=camp"
        local -r CAMP_URL=$(printf ${GITHUB_URL} ${CAMP_VERSION})

        pip install git+${CAMP_URL} >> ${LOG_FILE} 2>&1
        if [ $? -eq 0 ]; then
            printf "CAMP (%s) ready.\n" "${CAMP_VERSION}"
        else
            printf "Error (see logs in).\n" ${LOG_FILE}
        fi
    fi
}


cleanup () {
    # Removing package 'python-2.7-minimal' breaks the system
    local PYTHON_PACKAGES=""
    if [[ "${PYTHON_VERSION}" =~ "^2" ]]
    then
        PYTHON_PACKAGES=python3 python3.5-minimal python-pkg-resources
    fi
    local -r BUILD_PACKAGES=(\
                             curl \
                             unzip \
                             gnupg \
                             gnupg2 \
                             openssl \
                             git \
                             perl \
                             ca-certificates \
                             apt-transport-https \
                             software-properties-common \
                             ${PYTHON_PACKAGES} \
                             python-pip \
        )
    for each in "${BUILD_PACKAGES[@]}"
    do
        apt-get purge -y --allow-remove-essential $each >> ${LOG_FILE} 2>&1
    done
    apt-get autoremove -y >> ${LOG_FILE} 2>&1
    rm -rf /var/lib/apt/lists/*

    #ln -s /usr/bin/python2.7 /usr/bin/python
    if [[ "${DEBUG}" == "false" ]]
    then
        rm -rf ${LOG_FILE}
    fi
}



# -------------------------- MAIN SCRIPT --------------------------------
trap abort ERR

parse_arguments $*

if [[ "${DEBUG}" == "true" ]]
then
    set -o xtrace
fi

echo "" > ${LOG_FILE}

apt-get update -qq

ensure_CAMP_available

cleanup
