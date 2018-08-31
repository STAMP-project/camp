from abc import ABCMeta
from abc import abstractmethod


class ABCConfigRoot(object):
	
	__metaclass__ = ABCMeta

class ABCDockerImages(object):

	__metaclass__ = ABCMeta

class ABCDockerCompose(object):

	__metaclass__ = ABCMeta

class ABCExperiment(object):
	
	__metaclass__ = ABCMeta



class ABCConfigVisitor(object):

	def visit_docker_images(self, visitee):
		pass

	def visit_docker_compose(self, visitee):
		pass

	def visit_experiment(self, visitee):
		pass


class ABCConfigVisitee(object):

	__metaclass__ = ABCMeta

	def accept(self, visitor, **kwargs):
		result = None
		if isinstance(self, ABCConfigRoot):
			result = visitor.visit_config(self, **kwargs)
		elif isinstance(self, ABCDockerImages):
			result = visitor.visit_config(self, **kwargs)
		else:
			print 'Unknown element to visit '
		return result