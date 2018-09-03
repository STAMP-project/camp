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

	_docker_images_sec = 'docker_images'
	_docker_images_sec_build = 'build_script'
	
	_docker_compose_sec = 'docker_compose'
	_docker_compose_sec_compose = 'compose_files'

	_exp_sec = 'experiment'
	_exp_sec_script = 'script'
	_exp_sec_params = 'params'

	def visit_config(self, visitee, **kwargs):
		visitee.images = kwargs.get('images')
		visitee.compose = kwargs.get('compose')
		visitee.experiment = kwargs.get('experiment')
		return visitee

	def visit_images(self, visitee, **kwargs):
		config=kwargs['config']
		docker_images_sec_build_val = config.get(_docker_images_sec, _docker_images_sec_build)
		if docker_images_sec_build_val:
			visitee.build_script = docker_images_sec_build_val
		return visitee

	def visit_compose(self, visitee, **kwargs):
		config = kwargs['config']
		compose_str = config.get(_docker_compose_sec, _docker_compose_sec_compose)
		if compose_str:
			visitee.compose_files = filter(lambda x: x, [x.strip() for x in compose_str.split(';')])
		return visitee

	def visit_experiment(self, visitee, **kwargs):
		config = kwargs['config']
		exp_sec_script_val = config.get(_exp_sec, _exp_sec_script)
		exp_sec_params_val = config.get(_exp_sec, _exp_sec_params)
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
		result = _config.read(_file)

		if len(result):
			return None

		docker_images_obj = ConfigModelFactory().create_docker_images()
		docker_compose_obj = ConfigModelFactory().create_docker_compose()
		experiment_obj = ConfigModelFactory().create_experiment()
		config_obj = ConfigModelFactory().create_config()

		docker_images_obj.accept(self.visitor, config=_config)
		docker_compose_obj.accept(self.visitor, config=_config)
		experiment_obj.accept(self.visitor, config=_config)
		config_obj.accept(self.visitor, images=docker_compose_obj, compose=docker_compose, experiment=experiment_obj)
		
		return config_obj

