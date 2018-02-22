from abc import ABCMeta
from abc import abstractmethod


class Visitee(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def accept(visitor):
		pass

class ABCRealizationNode(Visitee):

	__metaclass__ = ABCMeta