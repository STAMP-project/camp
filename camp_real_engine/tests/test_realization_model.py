import yaml
import unittest

from camp_real_engine.plugins.model.realization import YamlRealizationModel


class TestRealizationModel(unittest.TestCase):

	def setUp(self):
		self.realization_yaml = '''
- variable1:
  - value1:
    - substituion1:
       type: regexp
       filename: "/name/Dockerfile"
       placement: "some_string"
       replacement: "another_string"
    - substituion2:
       type: regexp
       filename: "/name/Dockerfile1"
       placement: "some_string"
       replacement: "another_string"
  - value2:
    - substituion1:
       type: regexp
       filename: "/name/Dockerfile"
       placement: "some_string"
       replacement: "another_string"
'''

	def test_realization_model(self):
		yaml_obj = yaml.load(self.realization_yaml)

		real_model = YamlRealizationModel()
		real_model.parse(yaml_obj)

		variable_list = real_model.get_variables()
		self.assertIsNotNone(variable_list)
		self.assertTrue(len(variable_list) == 1)
		variable = variable_list[0]
		variable_name = variable.get_variable_label()
		self.assertEqual(variable_name, 'variable1')

		values = real_model.get_values_by_variable(variable)
		self.assertIsNotNone(values)
		self.assertTrue(len(values) == 2)
		value = values[0]
		value_label = value.get_value_label()
		self.assertEqual(value_label, 'value1')

		substitutions = real_model.get_substs_by_value(value)
		self.assertIsNotNone(substitutions)

		self.assertTrue(len(substitutions) == 2)
		substitution1, substitution2 = substitutions[0], substitutions[1]
		self.assertEqual(substitution1.get_subst_label(), 'substituion1')
		self.assertEqual(substitution2.get_subst_label(), 'substituion2')

		self.assertEqual(substitution1.get_type(),'regexp')
		self.assertEqual(substitution2.get_type(), 'regexp')

		self.assertEqual(substitution1.get_file_name(), '/name/Dockerfile')
		self.assertEqual(substitution2.get_file_name(), '/name/Dockerfile1')

		self.assertEqual(substitution1.get_placement_str(), 'some_string')
		self.assertEqual(substitution2.get_placement_str(), 'some_string')

		self.assertEqual(substitution1.get_replacement_str(), 'another_string')
		self.assertEqual(substitution2.get_replacement_str(), 'another_string')