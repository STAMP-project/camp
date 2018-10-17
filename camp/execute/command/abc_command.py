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


class ABCCommand(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def execute(self):
		pass

	@property
	def status(self):
		return self._status

	@property
	def logs(self):
		return self._logs
	

class ABCRunner(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def run(self):
		pass

	@abstractmethod
	def get_result(self):
		pass

class ABCRunnerKillable(ABCRunner):

	__metaclass__ = ABCMeta

	@abstractmethod
	def kill(self):
		pass
