import yaml
import unittest

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.utils.parsers.substitutions.subs_textfile_parser import RegExpFileSubstParser



class DummySubstParser(object):


	def __init__(self):
		self.file_contents = '''
		FROM ubuntu:some_string
		RUN cp ~/something ~/something_else
		'''
	
	def parse(self, subst_obj):
		return  True

	def get_file_content(self):
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

	def test_simple_substitution(self):
		self.dummy_subst_parser = DummySubstParser()
		self.regexp = RegExp(_parser_subst = self.dummy_subst_parser)
		self.regexp.execute_subst(self.substitution)
		self.assertTrue(self.expected_file_contents == self.dummy_subst_parser.get_file_content(), 'failed to perform substitution')

	def test_reg_exp_file_subst(self):
		obj = yaml.load(self.substitution)
		subs_parser = RegExpFileSubstParser()
		is_regexp = subs_parser.parse(obj)
		self.assertTrue(is_regexp, "faled to recognize regexp subst")

		self.assertTrue("some_string" == subs_parser.get_placement_str())
		self.assertTrue("another_string" == subs_parser.get_replacement_str())
		self.assertTrue("/name/Dockerfile" == subs_parser.get_file_name())
