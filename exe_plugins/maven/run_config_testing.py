#!/usr/bin/python
import os
import sys
import StringIO
import shutil
import ConfigParser
import subprocess

CONFIG_NAME = 'config.ini'
TEST_SUIT_NAME = 'category_name'
TEST_SUIT_SCRIPT = 'category_test_script'
TEST_SUIT_REPORT_FOLDER = 'report'
TEST_SUIT_LOG = 'logs.log'


def print_std(category, stdout, stderr):
	for line in StringIO.StringIO(stdout).readlines():
		print "[STDOUT " + category + "] " + line.rstrip()

	for line in StringIO.StringIO(stderr).readlines():
		print "[STDERR " + category + "] " + line.rstrip()

def folder_path(parent, child):
	parent = parent.strip()
	child = child.strip()
	return os.path.join(parent, child)

def copy_dir_contents(src, dst, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
 			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

def execute_testing(working_dir, global_report_dir, sut_dir, sut_config_testing_dir):
	config_parser = ConfigParser.RawConfigParser()
	config_parser.read(os.path.join(sut_config_testing_dir, CONFIG_NAME))

	test_suits = {}

	#preparing test suits
	for section in config_parser.sections():
		test_suit_name = config_parser.get(section, TEST_SUIT_NAME)
		test_suit_script = config_parser.get(section, TEST_SUIT_SCRIPT)

		test_suit_scrip_path = os.path.join(folder_path(sut_config_testing_dir, test_suit_name), test_suit_script)

		test_suit_working_folder = folder_path(working_dir, test_suit_name)
		os.mkdir(test_suit_working_folder)
		test_suit_report_folder = folder_path(test_suit_working_folder, TEST_SUIT_REPORT_FOLDER)
		os.mkdir(test_suit_report_folder)

		test_suit_data = {}
		test_suit_data['script'] = test_suit_scrip_path
		test_suit_data['working_folder'] = test_suit_working_folder
		test_suit_data['report_folder'] = test_suit_report_folder

		test_suits[test_suit_name] = test_suit_data

	#running jobs as subprocesses
	for key, value in test_suits.iteritems():
		command = [value['script'], key, value['working_folder'], value['report_folder'], sut_dir]
		print "Starting: " + " ".join(command)
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		test_suits[key]['proc'] = proc

	#waiting for all jobs to be completed and writing to log file
	for key, value in test_suits.iteritems():
		stdout, stderr = value['proc'].communicate()
		print_std(key, stdout, stderr)
		log_file = folder_path(value['report_folder'], TEST_SUIT_LOG) 
		with open(log_file, 'w') as file:
			for line in StringIO.StringIO(stdout).readlines():
				file.write(line)
			for line in StringIO.StringIO(stderr).readlines():
				file.write(line)
		dest_folder = folder_path(global_report_dir, key)
		os.mkdir(dest_folder)
		shutil.copy2(log_file, os.path.join(dest_folder, TEST_SUIT_LOG))
		#copy final report to global report directory
		final_report_folder = folder_path(value['report_folder'], key)
		if os.path.isdir(final_report_folder): 
			copy_dir_contents(final_report_folder, dest_folder)

	#preparing global report
	body_contents, header_contents, litem_contents, footer_contents = "", "", "", ""
	header_location = folder_path(folder_path(sut_config_testing_dir, "html_report_templates"), "header.html")
	footer_location = folder_path(folder_path(sut_config_testing_dir, "html_report_templates"), "footer.html")
	litem_location = folder_path(folder_path(sut_config_testing_dir, "html_report_templates"), "listitem.html")

	with open(header_location, 'r') as file:
		header_contents = file.read()

	with open(footer_location, 'r') as file:
		footer_contents = file.read()

	with open(litem_location, 'r') as file:
		litem_contents = file.read()

	for key, value in test_suits.iteritems():
		status = 'SUCCESS (LOG)'
		if value['proc'].returncode != 0:
			status = 'FAILURE (LOG)'

		item = litem_contents.replace('category_name_results', key)
		item = item.replace('category_link', folder_path(key, 'results.html'))
		item = item.replace('category_status', status)
		item = item.replace('category_logs_status', folder_path(key, TEST_SUIT_LOG))
		body_contents = body_contents + item

	final_report_contents = header_contents + body_contents + footer_contents
	with open(folder_path(global_report_dir, 'index.html'), 'w') as file:
		file.write(final_report_contents)


def generate_environments(sut_config_testing_dir, env_list_dir):
	print "Generating environments"
	to_replace = "%(env)s"
	to_replace_config_env = "%(tool)s"
	tool_name = os.path.basename(sut_config_testing_dir.replace(os.path.basename(sut_config_testing_dir), "").strip("/"))
	tmpl_config_contents, new_contig_contents = "", ""
	tmpl_env_dir = os.path.join(sut_config_testing_dir, "env_tmpl")
	config_file = os.path.join(sut_config_testing_dir, "config.ini")
	with open(config_file, 'r') as file:
		tmpl_config_contents = file.read()

	for item in os.listdir(env_list_dir):
		sub_dir = os.path.join(env_list_dir, item)
		if os.path.isdir(sub_dir):
			print "Generating from " + sub_dir
			env_dir = os.path.join(sut_config_testing_dir, item)
			shutil.copytree(tmpl_env_dir, env_dir)
			docker_env_dir = os.path.join(env_dir, "dockerfile")
			copy_dir_contents(sub_dir, docker_env_dir)
			new_contig_contents = new_contig_contents + tmpl_config_contents.replace(to_replace, item) + "\n"

			config_env_file = os.path.join(env_dir, "config.ini")
			tmpl_config_env_contents, new_config_env_contents = "", ""
			with open(config_env_file, 'r') as file:
				tmpl_config_env_contents = file.read()
			new_config_env_contents = tmpl_config_env_contents.replace(to_replace, item)
			new_config_env_contents = new_config_env_contents.replace(to_replace_config_env, tool_name)
			with open(config_env_file, 'w') as file:
				file.write(new_config_env_contents)

	with open(config_file, 'w') as file:
		file.write(new_contig_contents)


if __name__ == "__main__":
	working_dir = sys.argv[1]
	global_report_dir = sys.argv[2]
	sut_dir = sys.argv[3]
	sut_config_testing_dir = sys.argv[4]
	env_list_dir = sys.argv[5]

	generate_environments(sut_config_testing_dir, env_list_dir)
	execute_testing(working_dir, global_report_dir, sut_dir, sut_config_testing_dir)
	print "All test suits are completed!"