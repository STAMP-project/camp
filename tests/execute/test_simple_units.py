#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import unittest

from mock import patch, MagicMock, PropertyMock, call

from camp.execute.command.commands import Script, DockerComposeScript, DockerComposeScriptKillable

from camp.execute.parsers import ConfigINIParser
from camp.execute.model.config_model import ConfigRoot, DockerCompose, Experiment, PrePost



class TestSimpleUnits(unittest.TestCase):

	def setUp(self):

		mock_prepost = MagicMock(PrePost)
		mock_prepost.return_value.setup = "tests/execute/resources/setup.sh"

		mock_compose = MagicMock(DockerCompose)
		mock_compose.return_value.compose_files = ["tests/execute/resources/docker-compose.yml"]

		mock_experiment = MagicMock(Experiment)
		mock_experiment.return_value.script = "tests/execute/resources/experiment.sh"
		mock_experiment.return_value.params = "param1 param2"

		mock_config_root = MagicMock(ConfigRoot)
		mock_config_root.return_value.prepost = mock_prepost.return_value
		mock_config_root.return_value.compose = mock_compose.return_value
		mock_config_root.return_value.experiment = mock_experiment.return_value

		parser = MagicMock(ConfigINIParser)
		parser.return_value.parse.return_value = mock_config_root.return_value
		self.mocked_parser = parser.return_value


	@patch('os.path.isfile')
	@patch('camp.execute.command.commands.SimpleCommand')
	def test_script(self, mock_SimpleCommand, mock_isfile):
		mock_isfile.return_value = True
		script_obj = Script("tests/execute/resources/setup.sh")
		#also possible
		#mock_SimpleCommand.return_value.status = 0
		type(mock_SimpleCommand.return_value).status = PropertyMock(return_value=0)
		
		result = script_obj.run()
		commands = script_obj.get_result()

		mock_isfile.assert_called_once_with("tests/execute/resources/setup.sh")
		mock_SimpleCommand.return_value.execute.assert_called_once()
		expected_constr_call = [call(['./setup.sh'], 'tests/execute/resources')]
		self.assertEqual(mock_SimpleCommand.call_args_list, expected_constr_call)
		self.assertTrue(result)
		self.assertEqual(len(commands), 1)


	@patch('os.path.isfile')
	@patch('camp.execute.command.commands.SimpleCommand')
	def test_docker_compose_up_down(self, mock_SimpleCommand, mock_isfile):
		mock_isfile.return_value = True
		dcomp_script_obj = DockerComposeScript("tests/execute/resources/docker-compose.yml")
		dcomp_killable_script_obj = DockerComposeScriptKillable(dcomp_script_obj)
		mock_SimpleCommand.return_value.status = 0

		result = dcomp_script_obj.run()
		commads = dcomp_script_obj.get_result()

		mock_SimpleCommand.return_value.execute.assert_called_once()
		expected_constr_call = [call(['docker-compose', 'up', '-d'], 'tests/execute/resources')]
		self.assertEqual(mock_SimpleCommand.call_args_list, expected_constr_call)
		self.assertTrue(result)
		self.assertEqual(len(commads), 1)

		#kill services
		result = dcomp_killable_script_obj.kill()
		commads = dcomp_killable_script_obj.get_result()

		self.assertTrue(result)
		self.assertEqual(len(commads), 1)
		
		expected_execute_calls = [call.execute(), call.execute()]
		self.assertEqual(mock_SimpleCommand.return_value.method_calls, expected_execute_calls)
		expected_constr_call = [call(['docker-compose', 'up', '-d'], 'tests/execute/resources'),
			call(['docker-compose', 'down'], 'tests/execute/resources')]
		self.assertEqual(mock_SimpleCommand.call_args_list, expected_constr_call)


	def test_config_ini_parsing(self):
		config_file = "tests/execute/resources/config.ini"

		parser = ConfigINIParser()
		config = parser.parse(config_file)
		self.assertIsNotNone(config, 'failed to parse file at: ' + str(config_file))

		build_script = config.prepost.setup
		self.assertEqual(build_script, 'build/build.sh')
		self.assertFalse(config.prepost.setup_params)

		self.assertEqual(config.prepost.teardown, 'build/cleanup.sh')
		self.assertEquals(config.prepost.teardown_params, ['param1', 'param2'])

		compose_files = config.compose.compose_files
		self.assertEqual(len(compose_files), 2)

		exp_script = config.experiment.script
		self.assertEqual(exp_script, 'experiment/executeExp.sh')

		exp_params = config.experiment.params
		self.assertEqual(exp_params, ['param1', 'param2'])
