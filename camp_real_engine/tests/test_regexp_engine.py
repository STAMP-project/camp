import unittest
from unittest.mock import MagicMock

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.utils.parsers.substitutions.subs_textfile_parser import TextFileParser

class DummySubstParser(object):

	self.file_contents = '''
	FROM ubuntu:some_string
	RUN cp ~/something ~/something_else
	'''
	
	self.get_file_content(self):
		return set.file_contents


class TestRegExpEngine(unittest.TestCase):

	def setUp(self):
		pass

	def test_simple_substitution(self):

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
		
		self.mock_subst_parser = TextFileParser()
		self.mock_subst_parser.get_file_content = MagicMock(return_value = )

		self.regexp = RegExp(_parser_subst = self.dummy_subst_parser)
		self.regexp.execute_subst(self.substitution)

		self.assertTrue(self.expected_file_contents == self.dummy_subst_parser.get_file_content(), 'failed to perform substitution')

