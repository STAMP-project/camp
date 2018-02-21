import yaml
import unittest

from mock import MagicMock, patch

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.plugins.model.realization import RegExpFileSubstNode


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
