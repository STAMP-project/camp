import unittest

from mock import patch, MagicMock, PropertyMock, call

from core.command.commands import Script, DockerCompose

from core.parser.parsers import ConfigINIParser
from core.model.config_model import ConfigRoot, DockerCompose, Experiment, PrePost


class TestSimpleComp(unittest.TestCase):

	def setUp(self):

		mock_prepost = MagicMock(PrePost)
		mock_prepost.setup.return_value = "tests/resources/setup.sh"

		mock_compose = MagicMock(DockerCompose)
		mock_compose.compose_files.return_value = ["tests/resources/docker-compose.yml"]

		mock_experiment = MagicMock(Experiment)
		mock_experiment.script.return_value = "tests/resources/experiment.sh"
		mock_experiment.params.return_value = "param1 param2"

		mock_config_root = MagicMock(ConfigRoot)
		mock_config_root.prepost.return_value = mock_prepost
		mock_config_root.compose.return_value = mock_compose
		mock_config_root.experiment.return_value = mock_experiment

		self.parser = MagicMock(ConfigINIParser)
		self.parser.parse.return_value = mock_config_root

	@patch('os.path.isfile')
	@patch('core.command.commands.SimpleCommand')
	def test_script(self, mock_simple_command, mock_isfile):
		mock_isfile.return_value = True
		script_obj = Script("tests/resources/setup.sh")
		type(mock_simple_command.return_value).status = PropertyMock(return_value=0)
		
		result = script_obj.run()
		commands = script_obj.get_result()

		mock_isfile.assert_called_once_with("tests/resources/setup.sh")
		mock_simple_command.return_value.execute.assert_called_once()
		expected_constr_call = [call(['./setup.sh', ''], 'tests/resources')]
		self.assertEqual(mock_simple_command.call_args_list, expected_constr_call)
		self.assertTrue(result)
		self.assertEqual(len(commands), 1)


	@patch('core.command.commands.SimpleCommand')
	def test_docker_compose(self, mock_SimpleCommand):
		pass
		#compose_files = config.compose.compose_files
		#result = DockerCompose(compose_files[0]).run()
		#self.assertTrue(result.status)
		
		#result = Script(config.experiment.script, config.experiment.params).run()
		#self.assertTrue(result.status)

		#result = Script(config.prepost.teardown).run()
		#self.assertTrue(result.status)

	def test_config_ini_parsing(self):
		file = "tests/resources/config.ini"

		parser = ConfigINIParser()
		config = parser.parse(file)
		self.assertIsNotNone(config, 'failed to parse file at: ' + str(file))

		build_script = config.prepost.setup
		self.assertEqual(build_script, 'build/build.sh')

		compose_files = config.compose.compose_files
		self.assertEqual(len(compose_files), 2)

		exp_script = config.experiment.script
		self.assertEqual(exp_script, 'experiment/executeExp.sh')

		exp_params = config.experiment.params
		self.assertEqual(exp_params, 'param1 param2')