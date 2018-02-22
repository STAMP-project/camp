
class RegExpFileSubstNode(object):

	def parse(self, subst_obj):
		pass

	def get_subst_label(self):
		pass

	def get_file_name(self):
		return ''

	def get_placement_str(self):
		return ''

	def get_replacement_str(self):
		return ''


class VariableNode(object):

	def get_variable_label(self):
		pass


class ValueNode(object):

	def ger_value_label(self):
		pass


class YamlRealizationModel(object):

	def parse(self, subst_obj):
		pass

	def get_variables(self):
		pass

	def get_values_by_variable(self, variable):
		pass

	def get_substitutions_by_value(self, value):
		pass