import unittest

from core.parser.parsers import ConfigINIParser


class TestSimpleComp(unittest.TestCase):

	def test_docker_compose_exe(self):
		pass

	def test_config_ini_parsing(self):
		file = "tests/resources/config.ini"
		
		parser = ConfigINIParser()
		config = parser.parse(file)

		build_script = config.get_build_script()
		self.assertEqual(build_script, 'build/build.sh')

		compose_files = config.get_compose_files()
		self.assertEqual(len(compose_files), 2)

		exp_script = config.get_exp_script()
		self.assertEqual(exp_script, 'experiment/executeExp.sh')

		exp_params = config.get_exp_params()
		self.assertEqual(exp_params, 'param1 param2')