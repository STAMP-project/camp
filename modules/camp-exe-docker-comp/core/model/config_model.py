from core.model.abc_config_model import ABCConfigVisitee, ABCConfigRoot


class ConfigRoot(ABCConfigRoot, ABCConfigVisitee):

	def get_build_script(self):
		pass

	def get_compose_files(self):
		pass

	def get_exp_script(self):
		pass

	def get_exp_params(self):
		pass