import unittest

from core.command.commands import Script, DockerComposeScript, DockerComposeScriptKillable


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
