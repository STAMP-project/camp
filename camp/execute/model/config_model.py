#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.model.abc_config_model import ABCConfigVisitee, ABCConfigRoot, ABCPrePost, ABCDockerCompose, ABCExperiment



class Experiment(ABCExperiment, ABCConfigVisitee):

	def __init__(self, _script=None, _params=[]):
		self._script = _script
		self._params = _params

	@property
	def script(self):
		return self._script

	@script.setter
	def script(self, _script):
		self._script = _script
	
	@property
	def params(self):
		return self._params
	
	@params.setter
	def params(self, _params):
		self._params = _params


class DockerCompose(ABCDockerCompose, ABCConfigVisitee):

	def __init__(self, _compose_files=[]):
		self._compose_files = _compose_files

	@property
	def compose_files(self):
		return self._compose_files

	@compose_files.setter
	def compose_files(self, _compose_files):
		self._compose_files = _compose_files


class PrePost(ABCPrePost, ABCConfigVisitee):

	def __init__(self, _setup=None, _teardown=None, _setup_params=[], _teardown_params=[]):
		self._setup = _setup
		self._teardown = _teardown
		self._setup_params = _setup_params
		self._teardown_params = _teardown_params

	@property
	def setup(self):
		return self._setup

	@setup.setter
	def setup(self, _setup):
		self._setup = _setup

	@property
	def teardown(self):
		return self._teardown

	@teardown.setter
	def teardown(self, _teardown):
		self._teardown = _teardown

	@property
	def setup_params(self):
		return self._setup_params

	@setup_params.setter
	def setup_params(self, _setup_params):
		self._setup_params = _setup_params

	@property
	def teardown_params(self):
		return self._teardown_params

	@teardown_params.setter
	def teardown_params(self, _teardown_params):
		self._teardown_params = _teardown_params


class ConfigRoot(ABCConfigRoot, ABCConfigVisitee):

	def __init__(self, _prepost=None, _compose=None, _experiment=None):
		self._prepost = _prepost
		self._compose = _compose
		self._experiment = _experiment

	@property
	def prepost(self):
		return self._prepost

	@prepost.setter
	def prepost(self, _prepost):
		self._prepost = _prepost
	
	@property
	def compose(self):
		return self._compose

	@compose.setter
	def compose(self, _compose):
		self._compose = _compose

	@property
	def experiment(self):
		return self._experiment
	
	@experiment.setter
	def experiment(self, _experiment):
		self._experiment = _experiment
