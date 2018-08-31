import ConfigParser

from core.model.config_model import ConfigRoot


class ConfigModelFactory(object):

	def create_config(self):
		return ConfigRoot()


class ConfigINIParser(object):

	def __init__(self, _visitor=None):
		self.visitor = _visitor 

	def parse(self, _file):
		_config = ConfigParser.RawConfigParser()

		return ConfigRoot()

