import re

from camp_real_engine.plugins.abstract.abc_subst_realizer import ABC_subst_realizer
from camp_real_engine.utils.parsers.substitutions.subs_textfile_parser import RegExpFileSubstParser
from camp_real_engine.plugins.dao.daos import FileContentCommiter



class RegExp(ABC_subst_realizer):

	def __init__(self, _parser_subst = None, _content_commiter = None):
		self.parser_subst = _parser_subst if _parser_subst else RegExpFileSubstParser()
		self.content_commiter = _content_commiter if _content_commiter else FileContentCommiter()


	def execute_subst(self, substitution):
		if not self.parser_subst.parse(substitution):
			return

		file_content = self.content_commiter.read_content(self.parser_subst.get_file_name())
		placement = self.parser_subst.get_placement_str()
		replacement = self.parser_subst.get_replacement_str()

		pattern = re.compile(placement)
		match = pattern.search(file_content)
		if not match:
			return

		modified_content = re.sub(pattern, replacement, file_content)
		self.content_commiter.write_content(self.parser_subst.get_file_name())