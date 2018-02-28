import yaml
import unittest

class TestSimpleSubstitutins(unittest.TestCase):

	def setUp(self):

		self.realization_yaml_test_2_subs = '''
variables:
 - variable1:
    values:
     - value1:
        substitutions:
         - substituion1:
            type: regexp
            filename: "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/Dockerfile"
            placement: "jenkins:latest"
            replacement: "jenkins:lts"
         - substituion2:
            type: regexp
            filename: "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/Dockerfile"
            placement: "USER jenkins"
            replacement: ""
'''

		self.test_2_sub_tmp_path = "camp_real_engine/tests/resources/simple_e2e_regexp/tmp"
		self.test_2_sub_source_docker = "camp_real_engine/tests/resources/simple_e2e_regexp/Dockerfile"
		self.test_2_sub_first_sub = "camp_real_engine/tests/resources/simple_e2e_regexp/exp/Dockerfile_subst1"
		self.test_2_sub_second_sub = "camp_real_engine/tests/resources/simple_e2e_regexp/exp/Dockerfile_subst1_2"

	def test_two_substitutions(self):
		pass

	def tearDown(self):
		pass