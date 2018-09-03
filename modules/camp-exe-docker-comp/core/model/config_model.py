from core.model.abc_config_model import ABCConfigVisitee, ABCConfigRoot, ABCDockerImages, ABCDockerCompose, ABCExperiment



class Experiment(ABCExperiment, ABCConfigVisitee):

	def __init__(self, _script=None, _params=None):
		self._script = _script
		self._params = _params

	@property
	def script(self):
		return self._script

	@script.setter
	def set_script(self, _script):
		return self._script = _script
	
	@property
	def params(self):
		return self._params
	
	@params.setter
	def set_params(self, _params):
		return self._params = _params


class DockerCompose(ABCDockerCompose, ABCConfigVisitee):

	def __init__(self, _compose_files=[]):
		self._compose_files = _compose_files

	@property
	def compose_files(self):
		return self._compose_files

	@compose_files.setter
	def set(self, _compose_files):
		self._compose_files = _compose_files


class DockerImages(ABCDockerImages, ABCConfigVisitee):

	def __init__(self, _script):
		self._script = _script

	@property
	def build_script(self):
		return self._script
	
	@build_script.setter
	def set(self, _script):
		return self._script = _script


class ConfigRoot(ABCConfigRoot, ABCConfigVisitee):

	def __init__(self, _images=None, _compose=None, _experiment=None):
		self._images = _images
		self._compose = _compose
		self._experiment = _experiment

	@property
	def images(self):
		return self._images

	@images.setter
	def set_images(self, _images):
		self._images = _images
	
	@property
	def compose(self):
		return self._compose

	@compose.setter
	def set_compose(self, _compose):
		self._compose = _compose

	@property
	def experiment(self):
		return self._experiment
	
	@experiment.setter
	def sef_experiment(self, _experiment):
		self._experiment = _experiment