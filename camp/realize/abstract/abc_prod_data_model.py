#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from abc import ABCMeta, abstractmethod

from camp.realize.abstract.abc_visitor import Visitee



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
		result = None
		if isinstance(self, ABCProductRoot):
			result = visitor.visit_product_root(self, **kwagrs)
		elif isinstance(self, ABCProduct):
			result = visitor.visit_product(self, **kwagrs)
		elif isinstance(self, ABCProductReal):
			result = visitor.visit_product_real(self, **kwagrs)
		elif isinstance(self, ABCProductVar):
			result = visitor.visit_product_var(self, **kwagrs)
		else:
			print "Unknown node to visit: " + str(self)
		return result
