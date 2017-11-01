#!/bin/bash

SUT_URL="https://github.com/vassik/xwiki-platform.git"
SUT_NAME="xwiki-platform"

if [[ -d $SUT_NAME ]]; then
	echo "sut has been already downloaded, cleaning, updating..."
	cd $SUT_NAME
	git clean -fd
	git pull
else
	echo "sut has not beed downloaded..."
	git clone $SUT_URL
fi
