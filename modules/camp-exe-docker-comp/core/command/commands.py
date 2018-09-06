import os
import subprocess
import StringIO

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

	def __init__(self, _script_path, _script_pstr = None):
		self._script_path = _script_path
		self._script_pstr = _script_pstr or ''
		self.commands = []

	def run(self):
		if not os.path.isfile(self._script_path):
			return None

		dir_name = os.path.dirname(self._script_path)
		file_name = os.path.basename(self._script_path)

		cmd_array = ['./' + file_name, self._script_pstr]
		dir_name = dir_name or None

		command_obj = SimpleCommand(cmd_array, dir_name)
		command_obj.execute()
		self.commands.append(command_obj)
		return not command_obj.status

	def get_result(self):
		return self.commands


class DockerComposeScript(ABCRunner):

	def __init__(self, _docker_compose_path, _docker_compose_pstr = None):
		self._docker_compose_path = _docker_compose_path
		self._docker_compose_pstr = _docker_compose_pstr or ''
		self.commands = []

	def run(self):
		if not os.path.isfile(self._docker_compose_path):
			return None

		dir_name = os.path.dirname(self._docker_compose_path)
		cmd_array = ['docker-compose up -d', self._docker_compose_pstr]
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

	def run(self):
		commands = self.get_result()
		#only run if run command was not run
		if not len(commands):
			return self._docker_compose.run()

		return not commands[0].status

	def get_result(self):
		return self._docker_compose.get_result()

	def kill(self):
		commands = self.get_result()
		#only run if the run command was success
		if not (len(commands) and not commands[0].status):
			return False

		dir_name = os.path.dirname(self._docker_compose._docker_compose_path)
		cmd_array = ['docker-compose down']

		command_obj = SimpleCommand(cmd_array, dir_name)
		command_obj.execute()
		self._docker_compose.commands.append(command_obj)
		return not command_obj.status
