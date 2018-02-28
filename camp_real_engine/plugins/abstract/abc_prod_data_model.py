from abc import ABCMeta
from abc import abstractmethod

from camp_real_engine.plugins.abstract.abc_vistor import Visitee


class ABCProductRoot(object):

	__metaclass__ = ABCMeta


class ABCProduct(object):

	__metaclass__ = ABCMeta


class ABCProductReal(object):

	__metaclass__ = ABCMeta


class ABCProductVar(object):

	__metaclass__ = ABCMeta


class ABCProductVisitor(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def visit_product_root(self, visitee, **kwargs):
		pass

	@abstractmethod
	def visit_product(self, visitee, **kwargs):
		pass

	@abstractmethod
	def visit_product_real(self, visitee, **kwargs):
		pass

	@abstractmethod
	def visit_product_var(self, visitee, **kwargs):
		pass


class ABCProductRealNode(Visitee):

	__metaclass__ = ABCMeta

	def accept(self, visitor, **kwagrs):
		if isinstance(self, ABCProductRoot):
			visitor.visit_product_root(self, **kwagrs)
		elif isinstance(self, ABCProduct):
			visitor.visit_product(self, **kwagrs)
		elif isinstance(self, ABCProductReal):
			visitor.visit_product_real(self, **kwagrs)
		elif isinstance(self, ABCProductVar):
			visitor.visit_product_var(self, **kwagrs)
		else:
			print "Unknown node to visit: " + str(self)