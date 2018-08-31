import ConfigParser

from core.model.config_model import ConfigRoot
from core.model.abc_config_model import ABCConfigVisitor


class ConfigModelFactory(object):

	def create_config(self):
		return ConfigRoot()

class ConfigIniVisitor(ABCConfigVisitor):

	def set_init_config(self, _config):
		self.config = _config

	def visit_config(self, visitee, **kwargs):
		pass

	def visit_images(self, visitee, **kwargs):
		pass

	def visit_compose(self, visitee, **kwargs):
		pass

	def visit_experiment(self, visitee, **kwargs):
		pass

class ConfigINIParser(object):

	_docker_images_sec = 'docker_images'
	_docker_compose_sec = 'docker_compose'

	_exp_sec = 'experiment'
	_exp_sec_script = 'script'
	_exp_sec_params = 'params'

	def __init__(self, _visitor=None):
		self.visitor = _visitor or ConfigIniVisitor()

	def parse(self, _file):
		_config = ConfigParser.RawConfigParser()
		result = _config.read(_file)

		if len(result):
			return None
		self.visitor.set_init_config(self.config)

		_exp_sec_script_val = _config.get(_exp_sec, _exp_sec_script)


		return ConfigRoot()

