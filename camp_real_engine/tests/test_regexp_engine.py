import yaml
import unittest

from mock import MagicMock, patch

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.plugins.model.realization import RegExpFileSubstNode
from camp_real_engine.plugins.model.realization import YamlRealizationModel
from camp_real_engine.plugins.dao.daos import FileContentCommiter


class DummySubstParser(object):


	def __init__(self):
		self.file_contents = '''
		FROM ubuntu:some_string
		RUN cp ~/something ~/something_else
		'''
	
	def parse(self, subst_obj):
		return  True

	def get_file_name(self):
		return self.file_contents

	def get_placement_str(self):
		return 'some_string'

	def get_replacement_str(self):
		return 'another_string'

	def set_file_content(self, content):
		self.file_contents = content


class TestRegExpEngine(unittest.TestCase):

	def setUp(self):
		self.substitution = '''
substituion1: 
 type: regexp
 filename: "/name/Dockerfile"
 placement: "some_string"
 replacement: "another_string"
 '''

		self.init_file_contents = '''
		FROM ubuntu:some_string
		RUN cp ~/something ~/something_else
		'''

		self.expected_file_contents = '''
		FROM ubuntu:another_string
		RUN cp ~/something ~/something_else
		'''

		self.expected_file_name = "/name/Dockerfile"

		self.realization_yaml = '''
variables:
 -variable1:
   values:
    -value1:
      substitutions:
       -substituion1: 
         type: regexp
         filename: "/name/Dockerfile"
         placement: "some_string"
         replacement: "another_string"
       -substituion2:
         type: regexp
         filename: "/name/Dockerfile1"
         placement: "some_string"
         replacement: "another_string"
'''

	@patch('camp_real_engine.plugins.regexp.RegExpFileSubstNode')
	@patch('camp_real_engine.plugins.regexp.FileContentCommiter')
	def test_simple_substitution(self, mock_FileContentCommiter, mock_RegExpFileSubstNode):
		mock_regexp_subst = mock_RegExpFileSubstNode.return_value
		mock_regexp_subst.get_file_name.return_value = self.expected_file_name
		mock_regexp_subst.get_placement_str.return_value = "some_string"
		mock_regexp_subst.get_replacement_str.return_value = "another_string"
		mock_regexp_subst.parse.return_value = True

		mock_dao = mock_FileContentCommiter.return_value
		mock_dao.read_content.return_value = self.init_file_contents

		self.regexp = RegExp()
		self.regexp.execute_subst(self.substitution)
		mock_dao.write_content.assert_called_once_with(self.expected_file_name, self.expected_file_contents)

	def test_reg_exp_file_subst(self):
		obj = yaml.load(self.substitution)
		subs_parser = RegExpFileSubstNode()
		is_regexp = subs_parser.parse(obj)
		self.assertTrue(is_regexp, "faled to recognize regexp subst")

		self.assertTrue("some_string" == subs_parser.get_placement_str())
		self.assertTrue("another_string" == subs_parser.get_replacement_str())
		self.assertTrue("/name/Dockerfile" == subs_parser.get_file_name())

	def test_file_commiter(self):
		file_commiter = FileContentCommiter()
		content = file_commiter.read_content('/resouces/simple_e2e_regexp/Dockerfile')
		file_commiter.write_content('/resouces/simple_e2e_regexp/tmp/Dockerfile', content)
		saved_content = file_commiter.read_content('/resouces/simple_e2e_regexp/tmp/Dockerfile')

		self.assertTrue(content == saved_content, "files are not identical")


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
		self.assertTrue(len(values) == 1)
		value = values[0]
		value_label = value.get_value_label()
		self.assertEqual(value_label, 'value1')

		substitutions = real_model.get_substitutions_by_value(val)
		self.assertIsNotNone(substitutions)

		self.assertTrue(len(substitutions) == 2)
		substitution1, substitution2 = substitution[0], substitution[1]
		self.assertEqual(substituion1.get_subst_label(), 'substituion1')
		self.assertEqual(substituion2.get_subst_label(), 'substituion2')

		self.assertEqual(substitution1.get_type(),'regexp')
		self.assertEqual(substitution2.get_type(), 'regexp')

		self.assertEqual(substitution1.get_file_name(), '/name/Dockerfile')
		self.assertEqual(substitution2.get_file_name(), '/name/Dockerfile1')

		self.assertEqual(substitution1.get_placement_str(), 'some_string')
		self.assertEqual(substitution2.get_placement_str(), 'some_string')

		self.assertEqual(substitution1.get_replacement_str(), 'another_string')
		self.assertEqual(substitution2.get_replacement_str(), 'another_string')


