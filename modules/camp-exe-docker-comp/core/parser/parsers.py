import os
import ConfigParser

from core.model.config_model import ConfigRoot, DockerImages, DockerCompose, Experiment
from core.model.abc_config_model import ABCConfigVisitor


class ConfigModelFactory(object):

	def create_config(self):
		return ConfigRoot()

	def create_docker_images(self):
		return DockerImages()

	def create_docker_compose(self):
		return DockerCompose()

	def create_experiment(self):
		return Experiment()

class ConfigIniVisitor(ABCConfigVisitor):

	def __init__(self):
		self._docker_images_sec = 'docker_images'
		self._docker_images_sec_build = 'build_script'
		
		self._docker_compose_sec = 'docker_compose'
		self._docker_compose_sec_compose = 'compose_files'

		self._exp_sec = 'experiment'
		self._exp_sec_script = 'script'
		self._exp_sec_params = 'params'		

	def visit_config(self, visitee, **kwargs):
		visitee.images = kwargs.get('images')
		visitee.compose = kwargs.get('compose')
		visitee.experiment = kwargs.get('experiment')
		return visitee

	def visit_images(self, visitee, **kwargs):
		config=kwargs['config']
		docker_images_sec_build_val = config.get(self._docker_images_sec, self._docker_images_sec_build)
		if docker_images_sec_build_val:
			visitee.build_script = docker_images_sec_build_val
		return visitee

	def visit_compose(self, visitee, **kwargs):
		config = kwargs['config']
		compose_str = config.get(self._docker_compose_sec, self._docker_compose_sec_compose)
		if compose_str:
			visitee.compose_files = filter(lambda x: x, [x.strip() for x in compose_str.split(';')])
		return visitee

	def visit_experiment(self, visitee, **kwargs):
		config = kwargs['config']
		exp_sec_script_val = config.get(self._exp_sec, self._exp_sec_script)
		exp_sec_params_val = config.get(self._exp_sec, self._exp_sec_params)
		if exp_sec_script_val:
			visitee.script = exp_sec_script_val
		if exp_sec_params_val:
			visitee.params = exp_sec_params_val
		return visitee

class ConfigINIParser(object):

	def __init__(self, _visitor=None):
		self.visitor = _visitor or ConfigIniVisitor()

	def parse(self, _file):
		_config = ConfigParser.RawConfigParser()

		if not os.path.isfile(_file):
			print 'failed to locate file at:' + file
			return None

		result = _config.read(_file)
		if not len(result):
			print 'failed to parse config file at: ' + _file
			return None

		docker_images_obj = ConfigModelFactory().create_docker_images()
		docker_compose_obj = ConfigModelFactory().create_docker_compose()
		experiment_obj = ConfigModelFactory().create_experiment()
		config_obj = ConfigModelFactory().create_config()

		docker_images_obj.accept(self.visitor, config=_config)
		docker_compose_obj.accept(self.visitor, config=_config)
		experiment_obj.accept(self.visitor, config=_config)
		config_obj.accept(self.visitor, images=docker_images_obj, compose=docker_compose_obj, experiment=experiment_obj)
		return config_obj