import unittest

from core.parser.parsers import ConfigINIParser


class TestSimpleComp(unittest.TestCase):

	def test_docker_compose_exe(self):
		pass

	def test_config_ini_parsing(self):
		file = "tests/resources/config.ini"

		parser = ConfigINIParser()
		config = parser.parse(file)
		self.assertIsNotNone(config, 'failed to parse file at: ' + str(file))

		build_script = config.images.build_script
		self.assertEqual(build_script, 'build/build.sh')

		compose_files = config.compose.compose_files
		self.assertEqual(len(compose_files), 2)

		exp_script = config.experiment.script
		self.assertEqual(exp_script, 'experiment/executeExp.sh')

		exp_params = config.experiment.params
		self.assertEqual(exp_params, 'param1 param2')