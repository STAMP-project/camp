from camp_real_engine.plugins.abstract.abc_subst_realizer import ABC_subst_realizer
from camp_real_engine.utils.parsers.substitutions.subs_textfile_parser import TextFileParser



class RegExp(ABC_subst_realizer):

	def __init__(self, _parser_subst = None):
		self.parser_subst = _parser_subst if _parser_subst else TextFileParser()


	def execute_subst(self, substitution):
		self.parser_subst.parse(substitution)

		content = self.parser_subst.get_file_content()
		placement = self.parser_subst.get_placement_str()
		replacement = self.parser_subst.get_replacement_str()

		#do substitution here

		self.parser_subst.set_file_content(self.content)