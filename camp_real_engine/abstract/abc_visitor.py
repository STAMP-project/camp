from abc import ABCMeta
from abc import abstractmethod

class Visitee(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def accept(self, visitor, **kwagrs):
		pass