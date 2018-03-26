from abc import ABCMeta
from abc import abstractmethod


class ABC_subst_realizer(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def exe_subst(self, substitution):
		pass