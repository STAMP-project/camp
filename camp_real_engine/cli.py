import argparse

from camp_real_engine.engine import RealizationEngine


class CLI(object):

	def __init__(self):
		self.parser = argparse.ArgumentParser(prog='rcamp', description='CAMP Realization Tool')
		self.parser.add_argument('realize', nargs=1, help='realize is a command to start realization')
		self.parser.add_argument('path', nargs=1, help='path to file with with model to realize')


	def execute(self, command):
		parsed_args = self.parser.parse_args(command)
		args_dict = vars(parsed_args)
		command = args_dict.get('realize')[0]
		if command == 'realize':
			model_path = args_dict.get('path')[0]
			real_engine = RealizationEngine()
			products = real_engine.get_products(model_path)
			for product in products:
				real_engine.realize_product(product)
		else:
			self.parser.print_help()
