#!/usr/bin/env sh

set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace

USAGE=$(IFS='' cat <<'EOF'
Usage: sh install.sh [options...]
Options:
  -c, --camp-version STRING    Select a specific version of CAMP from Github.
                               Can be a branch name (e.g., 'master'), a tag, or
                               a commit hash. Default is 'master'.
  -l, --z3-platform            Install Z3 for a specific version of linux. 
                               Default is 'x64-debian-8.10'.
  -o, --only-z3                Does not install CAMP, but only the Z3 solver.
                               Default is 'false'.
  -p, --python-library DIR     Set the installation directory for the Z3 Python
                               bindings. Default is '/usr/lib/python2.7'.
  -z, --z3-version STRING      Set the version of the Z3 solver to install. 
                               Default is 4.7.1.
EOF
);


# Default parameters values

PYTHON_LIB_PATH=/usr/lib/python2.7
CAMP_VERSION=master
Z3_VERSION=4.7.1
Z3_PLATFORM=x64-debian-8.10
ONLY_DEPENDENCIES=false



unknown_option(){
    printf "Error: Unknown option '$1'.\n"
    printf "${USAGE}\n"
    exit 1
}



parse_arguments () {
    while [ $# -gt 0 ]; do
        case "$1" in
            -c|--camp-version)
                CAMP_VERSION="$2"
                shift 2
                ;;
            -l|--z3-platform)
                Z3_PLATFORM="$3"
                shift 2
                ;;
            -o|--only-z3)
                ONLY_DEPENDENCIES=true
                shift 1
                ;;
            -p|--python-library)
                PYTHON_LIB_PATH="$2"
                shift 2
                ;;
            -z|--z3-version)
                Z3_VERSION=$2
                shift 2
                ;;
            *)
                unknown_option "$1"
                break
                ;;
        esac
    done
}



version_of () {
    local -r tool=$1
    local -r flag=${2:-"--version"}
    local -r regex="[0-9]+(\.[0-9]+)+"
    local -r version=$($tool $flag | grep -Eo ${regex} | head -1)
    printf "%s\n" "$version"
}



ensure_curl_available() {
    if type curl >/dev/null 2>&1;
    then
        local -r version=$(version_of "curl")
        printf "Found curl '%s'.\n" $version
    else
        printf "Error: 'curl' is needed, by not available.\n";
        printf "You can install it using: 'apt-get install curl'.\n";
        exit 1;
    fi
}



ensure_git_available() {
    if type git >/dev/null 2>&1;
    then
        local -r version=$(version_of "git")
        printf "Found git '%s'.\n" $version
    else
        printf "Git is needed, but not available.\n";
        printf "You may want to install it using: 'apt-get install git'.\n";
        exit 1;
    fi
}



ensure_unzip_available() {
    if type unzip >/dev/null 2>&1;
    then
       local -r version=$(version_of "unzip" "-v")
       printf "Found unzip '%s'.\n" $version
    else
        printf "unzip is needed, but not available.\n";
        printf "You may want to install it using: 'apt-get install zip'.\n";
        exit 1;
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


test_compare_version () {
    result=$(compare_version $1 $2)
    printf "%s %s %s\n" $1 ${result} $2 >> install.log
}


ensure_pip_available() {
    local -r PIP_VERSION="19.0.3"
    if ! type pip >/dev/null 2>&1;
    then
        printf "PIP is not available, installing PIP ${PIP_VERSION}.\n";
        local -r PIP_INSTALLER_URL=https://bootstrap.pypa.io/get-pip.py
        \curl -sS -L -k -O ${PIP_INSTALLER_URL};
        python get-pip.py -qq pip==$PIP_VERSION;
        rm get-pip.py
        
    else
        local -r version_reqex="[0-9]+(\.[0-9]+)*"
        local -r current_version=$(version_of "pip")
        comparison=$(compare_version ${current_version} ${PIP_VERSION})
        if [ "$comparison" -eq "<" ];
        then
            printf "Pip '%s' not compatible. Upgrading to %s\n" ${current_version} ${PIP_VERSION}
            pip -qq install --upgrade pip==$PIP_VERSION
        fi   
    fi
}

test_Z3() {
    local -r TEST_Z3="z3 --version"
    if ${TEST_Z3} >/dev/null 2>&1; then
        printf "Z3 %s ready.\n" ${Z3_VERSION}
    else
        printf "Error: Z3 not working!\n";
        printf "Aborting.\n";
        exit 1;
    fi
}


test_Z3_python_bindings() {
    local -r TEST_PYTHON_BINDINGS="import z3; print(z3.get_version_string())"
    python -c "${TEST_PYTHON_BINDINGS}" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        printf "Z3 Python bindings ready. (%s)\n" ${PYTHON_LIB_PATH}
    else
        printf "Error: Z3 Bindings not working!\n";
        printf "Is '%s' the path to the Python's libraries?\n" ${PYTHON_LIB_PATH}
        printf "Aborting.\n";
        exit 1;
    fi
}


install_Z3() {
    ensure_unzip_available
    if ! type z3 >/dev/null 2>&1; then
        local -r Z3_ARCHIVE=z3-${Z3_VERSION}-${Z3_PLATFORM}.zip
        local -r Z3_URL="https://github.com/Z3Prover/z3/releases/download/z3-%s/%s"
        local -r Z3_ARCHIVE_URL=$(printf $Z3_URL $Z3_VERSION $Z3_ARCHIVE)
        local -r Z3_DIRECTORY=$(basename -s .zip $Z3_ARCHIVE)
        
        if ! [ -f ${Z3_ARCHIVE} ]; then
            \curl -sS -L -O ${Z3_ARCHIVE_URL}
        fi

        \unzip -q ${Z3_ARCHIVE}
        \mkdir --parents ${PYTHON_LIB_PATH}/z3/lib
        \cp ${Z3_DIRECTORY}/bin/z3 ${PYTHON_LIB_PATH}/z3/lib/
        \cp ${Z3_DIRECTORY}/bin/lib* $PYTHON_LIB_PATH/z3/lib/
        \cp -rf ${Z3_DIRECTORY}/bin/python/z3 ${PYTHON_LIB_PATH}
        \ln -s ${PYTHON_LIB_PATH}/z3/lib/z3 /usr/bin/z3
        \rm -rf ${Z3_DIRECTORY}
        \rm -rf ${Z3_ARCHIVE}

        test_Z3
        test_Z3_python_bindings
    fi
}


install_CAMP() {
    ensure_git_available
    ensure_pip_available

    local -r GITHUB_URL="https://github.com/STAMP-project/camp.git@%s#egg=camp"
    local -r CAMP_URL=$(printf ${GITHUB_URL} ${CAMP_VERSION})
    local -r LOG_FILE="camp_install.log"

    pip -qqq --log=${LOG_FILE} install git+${CAMP_URL}
    if [ $? -eq 0 ]; then
        printf "CAMP (%s) ready.\n" "${CAMP_VERSION}"
    else
        printf "Error (see logs in).\n" ${LOG_FILE}
    fi
}



# Main script
parse_arguments $*
ensure_curl_available
install_Z3

if [ "${ONLY_DEPENDENCIES}" == "false" ];
then
    install_CAMP
fi
