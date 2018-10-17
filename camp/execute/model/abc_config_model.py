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


class ABCConfigRoot(object):
	
	__metaclass__ = ABCMeta

class ABCPrePost(object):

	__metaclass__ = ABCMeta

class ABCDockerCompose(object):

	__metaclass__ = ABCMeta

class ABCExperiment(object):
	
	__metaclass__ = ABCMeta



class ABCConfigVisitor(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def visit_config(self, visitee, **kwargs):
		pass

	@abstractmethod
	def visit_prepost(self, visitee, **kwargs):
		pass

	@abstractmethod
	def visit_compose(self, visitee, **kwargs):
		pass

	@abstractmethod
	def visit_experiment(self, visitee, **kwargs):
		pass


class ABCConfigVisitee(object):

	__metaclass__ = ABCMeta

	def accept(self, visitor, **kwargs):
		result = None
		if isinstance(self, ABCConfigRoot):
			result = visitor.visit_config(self, **kwargs)
		elif isinstance(self, ABCPrePost):
			result = visitor.visit_prepost(self, **kwargs)
		elif isinstance(self, ABCDockerCompose):
			result = visitor.visit_compose(self, **kwargs)
		elif isinstance(self, ABCExperiment):
			result = visitor.visit_experiment(self, **kwargs)
		else:
			print 'Unknown element to visit: ' + str(self)
		return result
