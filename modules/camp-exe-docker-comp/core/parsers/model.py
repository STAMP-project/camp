from abc import ABCMeta
from abc import abstractmethod



class ABCConfigVisitor(object):

	def visit_docker_images(self, visitee):
		pass

	def visit_docker_compose(self, visitee):
		pass

	def visit_experiment(self, visitee):
		pass


class ConfigRoot(ABCConfigRoot, ABCConfigVisitee):

	pass
