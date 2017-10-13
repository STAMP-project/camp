#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See the NOTICE file distributed with this work for additional
# information regarding copyright ownership.
#
import os
import sys
import pwd
import ConfigParser
import subprocess
import StringIO
import shutil

CONFIG_NAME = 'config.ini'
CONFIG_GENERAL_SEC = 'general'

CONFIG_TESTING_SCRIPT = 'run_config_testing.py'

GENERAL_ROOT_TEST_FOLDER = 'root_test_folder'
GENERAL_TEST_WORKING_FOLDER = 'test_working_folder'
GENERAL_GLOBAL_REPORT_DIR = 'global_report_dir'
GENERAL_SYSTEM_UNDER_TEST = 'system_under_test'
GENERAL_SUT_CONFIG_TESTING_FOLDER = 'sut_config_testing_folder'

SCRIP_ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))


def print_std(stdout, stderr):
	for line in StringIO.StringIO(stdout).readlines():
		print "[STDOUT] " + line.rstrip()

	for line in StringIO.StringIO(stderr).readlines():
		print "[STDERR] " + line.rstrip()

def folder_path(parent, child):
	parent = parent.strip()
	child = child.strip()
	return os.path.join(parent, child)

def execute_framework():
	root_test_folder = SCRIP_ABSOLUTE_PATH

	config = ConfigParser.RawConfigParser()
	config.read(os.path.join(root_test_folder, CONFIG_NAME))

	test_working_folder = config.get(CONFIG_GENERAL_SEC, GENERAL_TEST_WORKING_FOLDER)
	global_report_dir = config.get(CONFIG_GENERAL_SEC, GENERAL_GLOBAL_REPORT_DIR)
	system_under_test = config.get(CONFIG_GENERAL_SEC, GENERAL_SYSTEM_UNDER_TEST)
	config_testing_folder = config.get(CONFIG_GENERAL_SEC, GENERAL_SUT_CONFIG_TESTING_FOLDER)

	full_test_working_folder = folder_path(root_test_folder, test_working_folder)
	full_global_report_dir = folder_path(root_test_folder, global_report_dir)
	full_system_under_test_dir = folder_path(root_test_folder, system_under_test)
	full_config_testing_dir = folder_path(full_system_under_test_dir, config_testing_folder)

	#clean working directory and clean directories
	if os.path.isdir(full_test_working_folder):
		shutil.rmtree(full_test_working_folder)
	os.makedirs(full_test_working_folder)

	if os.path.isdir(full_global_report_dir):
		shutil.rmtree(full_global_report_dir)
	os.makedirs(full_global_report_dir)

	full_config_testing_script = os.path.join(full_config_testing_dir, CONFIG_TESTING_SCRIPT)
	command = [full_config_testing_script, full_test_working_folder, full_global_report_dir, full_system_under_test_dir, full_config_testing_dir]
	print "Staring: " + " ".join(command)
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	print_std(stdout, stderr)


if __name__ == "__main__":
	execute_framework()
	print "Done!"