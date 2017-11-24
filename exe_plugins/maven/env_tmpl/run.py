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


import re
import os
import sys
import shutil
import StringIO
import subprocess
import ConfigParser
import xml.etree.ElementTree as ET

CONFIG_NAME = 'config.ini'
SCRIPT_ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_SECTION = 'runConfiguration'
RESOURCE_ARCH_NAME = 'resources.tar'

SETTING_DOKCERFILE_PATH = 'docker_image_dir'
SETTING_IMAGE_NAME = 'docker_image_name'



def copy_dir_contents(src, dst, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
 			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)


def print_job_std(stdout, stderr):
	for line in StringIO.StringIO(stdout).readlines():
		print '[STDOUT] ' + line.rstrip()

	for line in StringIO.StringIO(stderr).readlines():
		print '[STDERR] ' + line.rstrip()


def check_and_print_sdt(stdout, stderr):
	for line in StringIO.StringIO(stdout).readlines():
		print line.rstrip()

	if stderr:
		sys.stderr.write(stderr)
		sys.exit(1)


def build_docker_image(dockerfile_path, docker_image_name, sut_folder):
	dockerfile_abs = os.path.join(SCRIPT_ABSOLUTE_PATH, dockerfile_path)

	print "Copying SUT from " + sut_folder
	ignore_config_testing = lambda directory, contents: ['config-testing', '.git'] \
		if (os.path.isdir(os.path.join(directory, 'config-testing')) and 'config-testing' in contents) or \
			(os.path.isdir(os.path.join(directory, '.git')) and '.git' in contents) else []

	shutil.copytree(sut_folder, os.path.join(dockerfile_abs, "sut"), symlinks=False, ignore=ignore_config_testing)
	
	command = ['docker', 'build', '--rm', '-t', docker_image_name, '.']
	print 'Building image: ' + ' '.join(command) + ' in ' + dockerfile_abs
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dockerfile_abs)
	stdout, stderr = proc.communicate()
	check_and_print_sdt(stdout, stderr)



def get_master_ip_address():
	command = ['hostname', '-i']
	print "Find out master IP: " + ' '.join(command)
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	sys.stdout.write(stdout)
	sys.stderr.write(stderr)
	if not stdout:
		sys.stderr.write("Stdout for '" + " ".join(command) + "' is empty\n")
		return ''

	match = re.search("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", stdout)
	master_ip = '' if not match else match.group(0)
	if not master_ip:
		sys.stderr.write("Cannot find ip address of the master in stdout of '" + " ".join(command) + "': '" + stdout + "'\n")
	return master_ip


def execute_tests(**slave_params):
	script = slave_params.get('script')
	master_job_root = slave_params.get('master_job_root')
	master_ip = slave_params.get('master_ip')
	master_ssh_port = slave_params.get('master_ssh_port')
	master_user = slave_params.get('master_user')
	master_pass = slave_params.get('master_pass')
	docker_worker_image = slave_params.get('docker_worker_image')
	processes = {}

	
	#docker run --rm vassik/thingml-test-worker:v0.1 ./dojob.py /master/ 172.17.0.6 22 thmlslave thmlslave
	command = ['docker', 'run', '--rm', docker_worker_image, script, master_job_root,
		master_ip, master_ssh_port, master_user, master_pass]
	print 'Executing: ' + ' '.join(command)
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	#wait for all jobs to complete
	stdout, stderr = process.communicate()
	print_job_std(stdout, stderr)


def prepare_report(working_folder,report_folder, category_name):
	#we expect archive with results in tmp.tar
	header_accumulated_result = ''
	body_accumulated_result = ''
	footer_accumulated_result = ''
	category_report_folder = os.path.join(report_folder, category_name)
	os.mkdir(category_report_folder)


	command= ['tar', '-xf', 'tmp.tar']
	print "Executing: '" + ' '.join(command) + "' in " + working_folder
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_folder)
	stderr, stdout = proc.communicate()
	check_and_print_sdt(stdout, stderr)

	#copying content of the job result folder to the folder that accumulates results for the entity category
	copy_dir_contents(os.path.join(working_folder, 'tmp'), category_report_folder)


def run_routine(category_name, working_folder, report_folder, master_slave_user, master_slave_pwd, master_ssh_port, sut_folder):
	config = ConfigParser.ConfigParser()
	config.read(os.path.join(SCRIPT_ABSOLUTE_PATH, CONFIG_NAME))

	dockerfile_path = config.get(CONFIG_SECTION, SETTING_DOKCERFILE_PATH)
	docker_image_name = config.get(CONFIG_SECTION, SETTING_IMAGE_NAME)



	master_ip = get_master_ip_address()
	if not master_ip:
		sys.exit(1)

	slave_params = {'script' : './dojob.py', 'master_job_root' : working_folder, 
		'master_ip' : master_ip, 'master_ssh_port': master_ssh_port , 'master_user' : master_slave_user,
		'master_pass' : master_slave_pwd, 'docker_worker_image' : docker_image_name}


	build_docker_image(dockerfile_path, docker_image_name, sut_folder)
	execute_tests(**slave_params)
	prepare_report(working_folder, report_folder, category_name)


if __name__ == "__main__":
	category_name = sys.argv[1]
	working_folder = sys.argv[2]
	report_folder = sys.argv[3]
	sut_folder = sys.argv[4]

	master_slave_user = os.environ.get('MASTER_SLAVE_USER')
	master_slave_pwd = os.environ.get('MASTER_SLAVE_PWD')
	master_ssh_port = os.environ.get('MASTER_SSH_PORT')

	if not master_slave_user:
		message = "MASTER_SLAVE_USER env variable is not set!. Exiting..."
		sys.stderr.write(message + '\n');
		sys.exit(1)

	if not master_slave_pwd:
		message = "MASTER_SLAVE_PWD env variable is not set!. Exiting..."
		sys.stderr.write(message + '\n');
		sys.exit(1)

	if not master_ssh_port:
		message = "MASTER_SSH_PORT env variable is not set!. Exiting..."
		sys.stderr.write(message + '\n');
		sys.exit(1)

	run_routine(category_name, working_folder, report_folder, master_slave_user, master_slave_pwd, str(master_ssh_port), sut_folder)
	
	sys.exit(0)
