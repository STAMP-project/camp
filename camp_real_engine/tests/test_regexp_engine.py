import unittest

from camp_real_engine.plugins.regexp import RegExp


class DummySubstParser(object):


	def __init__(self):
		self.file_contents = '''
			FROM ubuntu:some_string
			RUN cp ~/something ~/something_else
		'''
	
	def parse(self, subst_obj):
		pass

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

		self.dummy_subst_parser = DummySubstParser()
		self.regexp = RegExp(_parser_subst = self.dummy_subst_parser)
		self.regexp.execute_subst(self.substitution)

		self.assertTrue(self.expected_file_contents == self.dummy_subst_parser.get_file_content(), 'failed to perform substitution')

