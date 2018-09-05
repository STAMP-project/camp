import os
import subprocess
import StringIO

from core.command.abc_command import ABCCommand, ABCRunner

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


class Script(ABCRunner):

	def __init__(self, _script_path, _script_pstr = None):
		self._script_path = _script_path
		self._script_pstr = _script_pstr or ''
		self.command = []

	def run(self):
		if not os.path.isfile(self._script_path):
			return None

		dir_name = os.path.dirname(self._script_path)
		file_name = os.path.basename(self._script_path)

		cmd_array = ['./' + file_name, self._script_pstr]
		dir_name = dir_name or None

		command_obj = SimpleCommand(cmd_array, dir_name)
		command_obj.execute()
		self.command.append(command_obj)
		return not command_obj.status

	def get_result(self):
		return self.command


class DockerCompose(ABCRunner):

	def run(self):
		pass

	def get_result(self):
		pass