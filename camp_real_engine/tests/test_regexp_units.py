import os
import yaml
import unittest
import shutil

from mock import MagicMock, patch

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.plugins.model.realization import RegExpFileSubstNode
from camp_real_engine.plugins.dao.daos import FileContentCommiter


class TestRegExpElements(unittest.TestCase):


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

		self.tmp_path = "camp_real_engine/tests/resources/simple_e2e_regexp/tmp"

		if os.path.exists(self.tmp_path):
			shutil.rmtree(self.tmp_path)

		os.makedirs(self.tmp_path)


	@patch('camp_real_engine.plugins.regexp.FileContentCommiter')
	def test_regexp_substitution(self, mock_FileContentCommiter):
		mock_regexp_subst = MagicMock(RegExpFileSubstNode)
		mock_regexp_subst.get_type.return_value = "regexp"
		mock_regexp_subst.get_file_name.return_value = self.expected_file_name
		mock_regexp_subst.get_placement_str.return_value = "some_string"
		mock_regexp_subst.get_replacement_str.return_value = "another_string"

		mock_dao = mock_FileContentCommiter.return_value
		mock_dao.read_content.return_value = self.init_file_contents

		self.regexp = RegExp()
		self.regexp.exe_subst(mock_regexp_subst)
		mock_dao.write_content.assert_called_once_with(self.expected_file_contents)


	def test_file_commiter(self):
		file_commiter = FileContentCommiter()
		file_commiter.set_read_file('camp_real_engine/tests/resources/simple_e2e_regexp/Dockerfile')
		content = file_commiter.read_content()
		docker_file_path = os.path.join(self.tmp_path, 'Dockerfile')
		file_commiter.set_write_file(docker_file_path)
		file_commiter.write_content(content)
		file_commiter.set_read_file(docker_file_path)
		saved_content = file_commiter.read_content()

		self.assertTrue(content != '')
		self.assertTrue(content == saved_content, "files are not identical")

	def tearDown(self):
		if os.path.exists(self.tmp_path):
			shutil.rmtree(self.tmp_path)