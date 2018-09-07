import os
import subprocess
import StringIO

from core.utility.tools import output_message, output_message_error
from core.command.abc_command import ABCCommand, ABCRunner, ABCRunnerKillable


class SimpleCommand(ABCCommand):

	def __init__(self, _command_array, _command_wd=None):
		self._command_array = _command_array
		self._command_wd = _command_wd

	def execute(self):
		proc = subprocess.Popen(self._command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._command_wd)
		stdout, stderr = proc.communicate()
		self._status = proc.returncode

		self._logs = dict()
		self._logs['stdout'] = StringIO.StringIO(stdout).getvalue()
		self._logs['stderr'] = StringIO.StringIO(stderr).getvalue()

	@property
	def status(self):
		return self._status

	@property
	def logs(self):
		return self._logs
	

class Script(ABCRunner):

	def __init__(self, _script_path, _script_params = []):
		self._script_path = _script_path
		self._script_params = _script_params
		self.commands = []

	def run(self):
		if not os.path.isfile(self._script_path):
			return None

		dir_name = os.path.dirname(self._script_path)
		file_name = os.path.basename(self._script_path)

		cmd_array = ['./' + file_name]
		map(lambda x: cmd_array.append(x), self._script_params)
		dir_name = dir_name or None

		command_obj = SimpleCommand(cmd_array, dir_name)
		command_obj.execute()
		self.commands.append(command_obj)
		return not command_obj.status

	def get_result(self):
		return self.commands


class DockerComposeScript(ABCRunner):

	def __init__(self, _docker_compose_path, _docker_compose_pstr = []):
		self._docker_compose_path = _docker_compose_path
		self._docker_compose_pstr = _docker_compose_pstr
		self.commands = []

	def run(self):
		if not os.path.isfile(self._docker_compose_path):
			return None

		dir_name = os.path.dirname(self._docker_compose_path)
		cmd_array = ['docker-compose', 'up','-d']
		map(lambda x: cmd_array.append(x), self._docker_compose_pstr)
		dir_name = dir_name or None

		command_obj = SimpleCommand(cmd_array, dir_name)
		command_obj.execute()
		self.commands.append(command_obj)
		return not command_obj.status

	def get_result(self):
		return self.commands


class DockerComposeScriptKillable(ABCRunnerKillable):

	def __init__(self, _docker_compose):
		self._docker_compose = _docker_compose
		self.commands = []

	def run(self):
		return self.kill()

	def get_result(self):
		return self.commands

	def kill(self):
		commands = self._docker_compose.get_result()
		#only run if the run command was success
		if not (len(commands) and not commands[0].status):
			return None

		dir_name = os.path.dirname(self._docker_compose._docker_compose_path)
		cmd_array = ['docker-compose', 'down']

		command_obj = SimpleCommand(cmd_array, dir_name)
		command_obj.execute()
		self.commands.append(command_obj)
		return not command_obj.status


class ConductExperimentRunner(ABCRunner):

	def __init__(self, _config):
		self._config = _config
		self.commands = []

	def run(self):
		anyfailuer = True
		setup_script = Script(self._config.prepost.setup,
			self._config.prepost.setup_params)
		result = setup_script.run()
		map(lambda x: self.commands.append(x), setup_script.get_result())

		command = (result == True or result == False) and setup_script.get_result()[0] or None
		command and output_message(command.logs['stdout'])
		command and output_message_error(command.logs['stderr'])
		if not result:
			command and output_message_error('Aborting: failed to execute setup script at: ' \
				+ self._config.prepost.setup) or \
					output_message_error('Aborting: failed to locate setup script at:' \
						+ self._config.prepost.setup)
			return False

		for compose_file in self._config.compose.compose_files:
			docker_up = DockerComposeScript(compose_file)
			result = docker_up.run()
			map(lambda x: self.commands.append(x), docker_up.get_result())

			command = (result == True or result == False) and docker_up.get_result()[0] or None
			command and output_message(command.logs['stdout'])
			command and output_message_error(command.logs['stderr'])
			if not result:
				command and output_message_error('Skipping: failed to execute docker-compose up: ' \
					+ compose_file) or \
						output_message_error('Skipping: failed to locate docker-compose script:' \
							+ compose_file)
				anyfailuer = False
				continue

			exp_script = Script(self._config.experiment.script,
				self._config.experiment.params)
			result = exp_script.run()
			map(lambda x: self.commands.append(x), exp_script.get_result())

			command = (result == True or result == False) and exp_script.get_result()[0] or None
			command and output_message(command.logs['stdout'])
			command and output_message_error(command.logs['stderr'])
			if not result:
				command and output_message_error('Failed to execute experiment script at: ' \
					+ self._config.experiment.script) or \
						output_message_error('Failed to locate experiment script at:' \
							+ self._config.experiment.script)
				anyfailuer = False

			docker_down = DockerComposeScriptKillable(docker_up)
			result = docker_down.run()
			map(lambda x: self.commands.append(x), docker_down.get_result())

			command = (result == True or result == False) and docker_down.get_result()[0] or None
			command and output_message(command.logs['stdout'])
			command and output_message_error(command.logs['stderr'])
			if not result:
				command and output_message_error('Skipping: failed to execute docker-compose down: ' \
					+ compose_file) or \
						output_message_error('Skipping: failed to execute docker-compose down:' \
							+ compose_file + ' due to docker-compose up is not succesfully completed')
				anyfailuer = False
	
		teardown_script = Script(self._config.prepost.teardown,
			self._config.prepost.teardown_params)
		result = teardown_script.run()
		map(lambda x: self.commands.append(x), teardown_script.get_result())

		command = (result == True or result == False) and teardown_script.get_result()[0] or None
		command and output_message(command.logs['stdout'])
		command and output_message_error(command.logs['stderr'])
		if not result:
			command and output_message_error('Failed to clean up: ' \
				+ self._config.prepost.teardown) or \
					output_message_error('Failed to locate clean up script: ' \
						+ self._config.prepost.teardown)
			anyfailuer = False

		return anyfailuer

	def get_result(self):
		return self.commands