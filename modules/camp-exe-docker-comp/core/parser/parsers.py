import os
import ConfigParser

from core.model.config_model import ConfigRoot, PrePost, DockerCompose, Experiment
from core.model.abc_config_model import ABCConfigVisitor
from core.utility.tools import output_message_error


class ConfigModelFactory(object):

	def create_config(self):
		return ConfigRoot()

	def create_prepost(self):
		return PrePost()

	def create_docker_compose(self):
		return DockerCompose()

	def create_experiment(self):
		return Experiment()

class ConfigIniVisitor(ABCConfigVisitor):

	def __init__(self):
		self._prepost_sec = 'pre_post'
		self._prepost_mapping = {
			'setup' : {'property' : 'setup'},
			'setup_params' : {'property' : 'setup_params', 'type' : 'array', 'delimiter' : ' '},
			'teardown' : {'property' : 'teardown'},
			'teardown_params' : {'property' : 'teardown_params', 'type' : 'array', 'delimiter' : ' '}
		}
		
		self._docker_compose_sec = 'docker_compose'
		self._docker_compose_mapping = {
			'compose_files' : {'property' : 'compose_files', 'type' : 'array', 'delimiter' : ';'}
		}

		self._exp_sec = 'experiment'
		self._exp_mapping = {
			'script' : {'property' : 'script'},
			'params' : {'property' : 'params', 'type' : 'array', 'delimiter' : ' '}
		}


	def _fill_in_object(self, objct, section, mapping, config):
		if not config.has_section(section):
			return

		for key, value in mapping.iteritems():
			if config.has_option(section, key):
				prop_name = value['property']
				option_value = config.get(section, key)
				if value.get('type') == 'array':
					delimiter = value['delimiter']
					option_value = filter(lambda x: x, [x.strip() for x in option_value.split(delimiter)])
				objct.__setattr__(prop_name, option_value)

	def visit_config(self, visitee, **kwargs):
		visitee.prepost = kwargs.get('prepost')
		visitee.compose = kwargs.get('compose')
		visitee.experiment = kwargs.get('experiment')
		return visitee

	def visit_prepost(self, visitee, **kwargs):
		self._fill_in_object(visitee, self._prepost_sec,
			self._prepost_mapping, kwargs['config'])
		return visitee

	def visit_compose(self, visitee, **kwargs):
		self._fill_in_object(visitee, self._docker_compose_sec,
			self._docker_compose_mapping, kwargs['config'])
		return visitee

	def visit_experiment(self, visitee, **kwargs):
		self._fill_in_object(visitee, self._exp_sec,
			self._exp_mapping, kwargs['config'])
		return visitee

class ConfigINIParser(object):

	def __init__(self, _visitor=None):
		self.visitor = _visitor or ConfigIniVisitor()

	def parse(self, _file):
		_config = ConfigParser.RawConfigParser()

		if not os.path.isfile(_file):
			output_message_error('failed to locate file at:' + str(file))
			return None

		result = _config.read(_file)
		if not len(result):
			output_message_error('failed to parse config file at: ' + _file)
			return None

		docker_images_obj = ConfigModelFactory().create_prepost()
		docker_compose_obj = ConfigModelFactory().create_docker_compose()
		experiment_obj = ConfigModelFactory().create_experiment()
		config_obj = ConfigModelFactory().create_config()

		docker_images_obj.accept(self.visitor, config=_config)
		docker_compose_obj.accept(self.visitor, config=_config)
		experiment_obj.accept(self.visitor, config=_config)
		config_obj.accept(self.visitor, prepost=docker_images_obj, compose=docker_compose_obj, experiment=experiment_obj)
		return config_obj