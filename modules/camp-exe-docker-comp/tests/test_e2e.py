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
		