from abc import ABCMeta
from abc import abstractmethod

from camp_real_engine.plugins.abstract.abc_vistor import Visitee


class ABCVariableNode(object):

	__metaclass__ = ABCMeta


class ABCValueNode(object):

	__metaclass__ = ABCMeta


class ABCSubstitutionNode(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def get_type(self):
		pass


class ABCRealVisitor(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def visit_variable_node(self, visitee, **kwagrs):
		pass

	@abstractmethod
	def visit_value_node(self, visitee, **kwagrs):
		pass

	@abstractmethod
	def visit_substitution_node(self, visitee, **kwagrs):
		pass


class ABCRealizationNode(Visitee):

	__metaclass__ = ABCMeta

	def accept(self, visitor, **kwagrs):
		if isinstance(self, ABCVariableNode):
			visitor.visit_variable_node(self, **kwagrs)
		elif isinstance(self, ABCValueNode):
			visitor.visit_value_node(self, **kwagrs)
		elif isinstance(self, ABCSubstitutionNode):
			visitor.visit_substitution_node(self, **kwagrs)
		else:
			print "Unknown node to visit: " + str(self)