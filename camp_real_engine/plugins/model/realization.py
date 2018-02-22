from camp_real_engine.plugins.abstract.abc_vistor import ABCRealizationNode




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


class VariableNode(ABCRealizationNode):

	def __init__(self, _instance = None):
		pass

	def get_variable_label(self):
		pass

	def add_value(self):
		pass


class ValueNode(object):

	def ger_value_label(self):
		pass


class ComponentFactory(object):

	def create_variable(self, _yaml_instance, _label = None):
		pass


class YamlRealizationModel(object):

	def __init__(self):
		self.cfacotry = ComponentFactory()

	def parse(self, yaml_obj):
		variables = yaml_obj['variables']
		for variable in variables:
			cvar = self.cfacotry.create_variable(yaml_obj['variables'], _label = variable)
			

	def get_variables(self):
		pass

	def get_values_by_variable(self, variable):
		pass

	def get_substitutions_by_value(self, value):
		pass