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


class ABC_subst_realizer(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def exe_subst(self, substitution):
		pass
