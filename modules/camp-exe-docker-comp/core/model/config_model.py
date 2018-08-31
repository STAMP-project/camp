from core.model.abc_config_model import ABCConfigVisitee, ABCConfigRoot, ABCDockerImages, ABCDockerCompose, ABCExperiment



class Experiment(ABCExperiment, ABCConfigVisitee):

	def __init__(self, _script, _params):
		self.script = _script
		self.params = _params

	def get_script(self):
		return self.script

	def get_params(self):
		return self.params

class DockerCompose(ABCDockerCompose, ABCConfigVisitee):

	def __init__(self, **kwargs):
		self.compose = dict()
		for key, value in kwargs.items():
			self.compose[key] = value

	def get_compose_files(self):
		return self.compose.values()

class DockerImages(ABCDockerImages, ABCConfigVisitee):

	def __init__(self, _script):
		self.script = _script

	def get_build_script():
		return self.script


class ConfigRoot(ABCConfigRoot, ABCConfigVisitee):

	def __init__(self, _images=None, _compose=None, _experiment=None):
		self.images = _images
		self.compose = _compose
		self.experiment = _experiment

	def get_build_script(self):
		return self.images and self.images.get_build_script()

	def get_compose_files(self):
		return self.compose and self.compose.get_compose_files()

	def get_exp_script(self):
		return self.experiment and self.experiment.get_script()

	def get_exp_params(self):
		return self.experiment and self.experiment.get_params()