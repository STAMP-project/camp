import os
import shutil
import yaml
import unittest

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.plugins.model.realization import YamlRealizationModel

class TestSimpleSubstitutins(unittest.TestCase):

	def setUp(self):

		self.realization_yaml_test_2_subs = '''
variable1:
 value1:
  operations:
   - substituion1:
      engine: regexp
      filename: "tests/resources/simple_e2e_regexp/tmp/Dockerfile"
      placement: "jenkins:latest"
      replacement: "jenkins:lts"
   - substituion2:
      engine: regexp
      filename: "tests/resources/simple_e2e_regexp/tmp/Dockerfile"
      placement: "USER jenkins"
      replacement: ""
'''

		self.test_2_sub_tmp_path = "tests/resources/simple_e2e_regexp/tmp"
		self.test_2_sub_source_docker = "tests/resources/simple_e2e_regexp/Dockerfile"
		self.test_2_sub_first_sub = "tests/resources/simple_e2e_regexp/exp/Dockerfile_subst1"
		self.test_2_sub_second_sub = "tests/resources/simple_e2e_regexp/exp/Dockerfile_subst1_2"


		with open(self.test_2_sub_first_sub, 'r') as file:
			self.exp_dockerfile_1_subst = file.read()

		with open(self.test_2_sub_second_sub, 'r') as file:
			self.exp_dockerfile_1_2_subst = file.read()

		if os.path.exists(self.test_2_sub_tmp_path):
			shutil.rmtree(self.test_2_sub_tmp_path)

		os.makedirs(self.test_2_sub_tmp_path)

		shutil.copy(self.test_2_sub_source_docker, self.test_2_sub_tmp_path)


	def test_two_substitutions(self):
		yaml_obj = yaml.load(self.realization_yaml_test_2_subs)
		real_model = YamlRealizationModel()
		real_model.parse(yaml_obj)

		variables = real_model.get_variables()
		values = real_model.get_values_by_variable(variables[0])
		substitutions = real_model.get_substs_by_value(values[0])

		regexp = RegExp()
		regexp.exe_subst(substitutions[0])

		tmp_dockerfile = os.path.join(self.test_2_sub_tmp_path, 'Dockerfile')
		dockerfile_content = ''
		with open(tmp_dockerfile, 'r') as file:
			dockerfile_content = file.read()
		
		self.assertEqual(dockerfile_content, self.exp_dockerfile_1_subst)

		regexp.exe_subst(substitutions[1])

		tmp_dockerfile = os.path.join(self.test_2_sub_tmp_path, 'Dockerfile')
		dockerfile_content = ''
		with open(tmp_dockerfile, 'r') as file:
			dockerfile_content = file.read()

		self.assertEqual(dockerfile_content, self.exp_dockerfile_1_2_subst)


	def tearDown(self):
		if os.path.exists(self.test_2_sub_tmp_path):
			shutil.rmtree(self.test_2_sub_tmp_path)