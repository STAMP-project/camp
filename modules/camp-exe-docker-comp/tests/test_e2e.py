import unittest

from core.command.commands import Script, DockerComposeScript
from core.command.commands import DockerComposeScriptKillable, ConductExperimentRunner
from core.parser.parsers import ConfigINIParser


class TestE2E(unittest.TestCase):

	def test_real_docker_compose_e2e(self):
		dcomp_script_obj = DockerComposeScriptKillable(
			DockerComposeScript("tests/resources/composetest/docker-compose.yml"))

		result = dcomp_script_obj.run()
		commads = dcomp_script_obj.get_result()

		self.assertTrue(result)
		self.assertEqual(len(commads), 1)
		print commads[0].logs

		result = dcomp_script_obj.kill()
		commads = dcomp_script_obj.get_result()

		self.assertTrue(result)
		self.assertEqual(len(commads), 2)
		print commads[1].logs

	def test_script_exe_e2e(self):
		script_obj = Script('tests/resources/scripts/script.sh', ['param1'])
		result = script_obj.run()
		commands = script_obj.get_result()

		self.assertTrue(result)
		self.assertEqual(len(commands), 1)
		self.assertEqual(commands[0].status, 0)

		stdout = commands[0].logs['stdout']
		stderr = commands[0].logs['stderr']
		expected_stdout = './script.sh param1'
		self.assertEqual(stdout.strip(), expected_stdout)
		self.assertEqual(stderr.strip(), '')

	def test_script_exe_failure_e2e(self):
		script_obj = Script('tests/resources/scripts/script_err.sh')
		result = script_obj.run()
		commands = script_obj.get_result()

		self.assertFalse(result)
		self.assertEqual(len(commands), 1)
		self.assertTrue(commands[0].status != 0)

		stdout = commands[0].logs['stdout']
		stderr = commands[0].logs['stderr']
		self.assertEqual(stdout.strip(), '')
		self.assertTrue(stderr.strip() != 0)

	def test_execution_composetest_e2e(self):
		file_path = 'tests/resources/config_composetest.ini'
		parser = ConfigINIParser()
		config = parser.parse(file_path)

		runner = ConductExperimentRunner(config)

		# run setup script, run docker compose up, run experiment, run docker down, run teardown script
		result = runner.run()

		self.assertTrue(runner)
		commands = runner.get_result()
		self.assertEqual(len(commands), 5)

		setup_command = commands[0]
		self.assertEqual(setup_command.status, 0)
		self.assertEqual(setup_command.logs['stdout'].strip(), 'setup! param1')
		self.assertEqual(setup_command.logs['stderr'].strip(), '')

		docker_setup_command = commands[1]
		self.assertEqual(docker_setup_command.status, 0)
		self.assertTrue(setup_command.logs['stdout'].strip() != '')
		self.assertEqual(setup_command.logs['stderr'].strip(), '')
		
		exp_command = commands[2]
		self.assertEqual(exp_command.status, 0)
		self.assertEqual(setup_command.logs['stdout'].strip(), 'Hello World! I have been seen 1 times. param1:param1 param2:param1')
		self.assertEqual(setup_command.logs['stderr'].strip(), '')

		docker_down_command = commands[3]
		self.assertEqual(docker_down_command.status, 0)
		self.assertTrue(docker_down_command.logs['stdout'].strip() != '')
		self.assertEqual(docker_down_command.logs['stderr'].strip(), '')

		teardown_command = commands[2]
		self.assertEqual(teardown_command.status, 0)
		self.assertEqual(teardown_command.logs['stdout'].strip(), 'teardown! param1')
		self.assertEqual(teardown_command.logs['stderr'].strip(), '')


