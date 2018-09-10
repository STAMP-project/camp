import argparse

from core.command.commands import ConductExperimentRunner
from core.parser.parsers import ConfigINIParser
from core.utility.tools import output_message


class CLI(object):

	def __init__(self):
		self.parser = argparse.ArgumentParser(prog='campexe', description='CAMP configuration execuion tool')
		self.parser.add_argument('docker-compose', nargs=1, help='"docker-compose" to execute docker-compose files')
		self.parser.add_argument('<config-file>', nargs=1, help='path to config file')

	def execute(self, command):
		parsed_args = self.parser.parse_args(command)
		args_dict = vars(parsed_args)
		command = args_dict.get('docker-compose')[0]
		if command == 'docker-compose':
			config_file = args_dict.get('<config-file>')[0]
			parser = ConfigINIParser()
			config = parser.parse(config_file)
			if not config:
				return

			experiment = ConductExperimentRunner(config)
			result = experiment.run()
			message = result and 'Completed with failures. Please check logs!' or 'Completed!'
			output_message(message)
		else:
			self.parser.print_help()
