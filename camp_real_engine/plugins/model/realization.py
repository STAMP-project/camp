from camp_real_engine.plugins.abstract.abc_vistor import ABCRealizationNode, ABCVariableNode, ABCValueNode, ABCSubstitutionNode
from camp_real_engine.plugins.abstract.abc_vistor import Visitor



class VariableNode(ABCRealizationNode, ABCVariableNode):

	def __init__(self, *args, **kwagrs):
		self.values = []
		self.label = None

	def set_variable_label(self, _label):
		self.label = _label

	def get_variable_label(self):
		return self.label

	def add_value_node(self, _value_node):
		self.values.append(_value_node)

	def get_value_nodes(self):
		return self.values


class ValueNode(ABCRealizationNode, ABCValueNode):

	def __init__(self, *args, **kwagrs):
		self.variable = None
		self.substitutions = []

	def get_value_label(self):
		return self.label

	def get_subst_nodes(self):
		return self.substitutions

	def set_value_label(self, _label):
		self.label = _label

	def set_variable_node(self, _variable):
		self.variable = _variable

	def add_subst_node(self, _substitution):
		self.substitutions.append(_substitution)


class RegExpFileSubstNode(ABCRealizationNode, ABCSubstitutionNode):

	def __init__(self, *args, **kwagrs):
		self.value, self.label, self.filename, self.placement, self.replacement = None, None, None, None, None

	def parse(self, subst_obj):
		pass

	def get_subst_label(self):
		return self.label

	def get_file_name(self):
		return self.replacement

	def get_placement_str(self):
		return self.placement

	def get_replacement_str(self):
		return self.replacement

	def set_subst_label(self, _label):
		self.label = _label

	def set_file_name(self, _filename):
		self.filename = _filename

	def set_placement_str(self, _placement):
		self.placement = _placement

	def set_replacement_str(self, _replacement):
		self.replacement = _replacement

	def set_value_node(self, _value):
		self.value = _value


class ComponentFactory(object):

	def create_variable(self, **kwagrs):
		return VariableNode()

	def create_value(self, **kwagrs):
		return ValueNode()

	def create_substitution(self, **kwagrs):
		return RegExpFileSubstNode()


class YamlVisitor(Visitor):

	def visit_variable_node(self, comp_var, **kwagrs):
		comp_var.set_variable_label(kwagrs['label'])

	def visit_value_node(self, comp_val, **kwagrs):
		comp_val.set_value_label(kwagrs['label'])
		comp_variable_node = kwagrs['var_node']
		comp_val.set_variable_node(comp_variable_node)
		comp_variable_node.add_value_node(comp_val)

	def visit_substitution_node(self, comp_subs, **kwagrs):
		label = kwagrs['label']
		comp_value_node = kwagrs['value_node']
		comp_subs.set_value_node(comp_value_node)
		comp_value_node.add_subst_node(comp_subs)

		comp_subs.set_subst_label(label)
		comp_subs.set_file_name(kwagrs['yaml_substitutions'][label]['filename'])
		comp_subs.set_placement_str(kwagrs['yaml_substitutions'][label]['placement'])
		comp_subs.set_replacement_str(kwagrs['yaml_substitutions'][label]['replacement'])


class YamlRealizationModel(object):

	def __init__(self):
		self.cfacotry = ComponentFactory()
		self.yaml_visitor = YamlVisitor()
		self.realization = []

	def parse(self, yaml_obj):
		variables = yaml_obj['variables']
		for variable in variables:
			cvar = self.cfacotry.create_variable()
			cvar.accept(self.yaml_visitor, yaml_vars = yaml_obj['variables'], label = variable)
			values = yaml_obj['variables'][variable]['values']
			for value in values:
				cvalue = self.cfacotry.create_value()
				cvalue.accept(self.yaml_visitor, var_node = cvar, yaml_values = values, label = value)
				substitutions = yaml_obj['variables'][variable]['values'][value]['substitutions']
				for substitution in substitutions:
					csubsitution = self.cfacotry.create_substitution()
					csubsitution.accept(self.yaml_visitor, value_node = cvalue, yaml_substitutions = substitutions, label = substitution)
			self.realization.append(cvar)

	def get_variables(self):
		return self.realization

	def get_values_by_variable(self, variable):
		return variable.get_value_nodes()

	def get_substs_by_value(self, value):
		return value.get_subst_nodes()