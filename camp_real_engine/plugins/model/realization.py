from camp_real_engine.plugins.abstract.abc_real_data_model import ABCRealizationNode, ABCVariableNode, ABCValueNode, ABCSubstitutionNode, ABCRealVisitor



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
		self.type = None
		self.value = None

	def get_value_type(self):
		return self.type

	def get_value_value(self):
		return self.value

	def get_value_label(self):
		return self.label

	def get_subst_nodes(self):
		return self.substitutions

	def set_value_label(self, _label):
		self.label = _label

	def set_variable_node(self, _variable):
		self.variable = _variable

	def set_value_type(self, _type):
		self.type = _type

	def set_value_value(self, _value):
		self.value = _value

	def add_subst_node(self, _substitution):
		self.substitutions.append(_substitution)


class RegExpFileSubstNode(ABCRealizationNode, ABCSubstitutionNode):

	def __init__(self, *args, **kwagrs):
		self.value, self.label, self.filename = None, None, None
		self.placement, self.replacement, self.type = None, None, None

	def get_subst_label(self):
		return self.label

	def get_file_name(self):
		return self.filename

	def get_placement_str(self):
		return self.placement

	def get_replacement_str(self):
		return self.replacement

	def get_type(self):
		return self.type

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

	def set_type(self, _type):
		self.type = _type


class ComponentFactory(object):

	def create_variable(self, **kwagrs):
		return VariableNode()

	def create_value(self, **kwagrs):
		return ValueNode()

	def create_substitution(self, **kwagrs):
		return RegExpFileSubstNode()


class YamlVisitor(ABCRealVisitor):

	def visit_variable_node(self, comp_var, **kwagrs):
		variable_label = kwagrs['yaml_var'].keys()[0]
		comp_var.set_variable_label(variable_label)

	def visit_value_node(self, comp_val, **kwagrs):
		comp_val.set_value_label(kwagrs['yaml_value'].keys()[0])
		comp_val.set_value_type(kwagrs['yaml_value'].values()[0].get('type'))
		comp_val.set_value_value(kwagrs['yaml_value'].values()[0].get('value'))
		comp_variable_node = kwagrs['var_node']
		comp_val.set_variable_node(comp_variable_node)
		comp_variable_node.add_value_node(comp_val)

	def visit_substitution_node(self, comp_subs, **kwagrs):
		yaml_subst = kwagrs['yaml_subst']
		comp_value_node = kwagrs['value_node']
		comp_subs.set_value_node(comp_value_node)
		comp_value_node.add_subst_node(comp_subs)

		subs_label = yaml_subst.keys()[0]
		comp_subs.set_subst_label(yaml_subst.keys()[0])
		comp_subs.set_file_name(yaml_subst[subs_label]['filename'])
		comp_subs.set_placement_str(yaml_subst[subs_label]['placement'])
		comp_subs.set_replacement_str(yaml_subst[subs_label]['replacement'])
		comp_subs.set_type(yaml_subst[subs_label]['engine'])


class YamlRealizationModel(object):

	def __init__(self):
		self.cfacotry = ComponentFactory()
		self.yaml_visitor = YamlVisitor()
		self.realization = []

	def parse(self, yaml_obj):
		for var_key, var_value in yaml_obj.iteritems():
			variable = dict()
			variable[var_key] = var_value
			cvar = self.cfacotry.create_variable()
			cvar.accept(self.yaml_visitor, yaml_var = variable)
			for val_key, val_value in var_value.iteritems():
				value = dict()
				value[val_key] = val_value
				cvalue = self.cfacotry.create_value()
				cvalue.accept(self.yaml_visitor, var_node = cvar, yaml_value = value)
				for substitution in val_value['operations']:
					csubsitution = self.cfacotry.create_substitution()
					csubsitution.accept(self.yaml_visitor, value_node = cvalue, yaml_subst = substitution)
			self.realization.append(cvar)

	def get_variables(self):
		return self.realization

	def get_values_by_variable(self, variable):
		return variable.get_value_nodes()

	def get_substs_by_value(self, value):
		return value.get_subst_nodes()

	def get_subst_by_var_val(self, var_val):
		for variable in self.realization:
			if variable.get_variable_label() == var_val[0]:
				values = variable.get_value_nodes()
				for value in values:
					if value.get_value_label() == var_val[1]:
						return value.get_subst_nodes()
		return []