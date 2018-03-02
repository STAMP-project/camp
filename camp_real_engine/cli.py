import argparse

from camp_real_engine.engine import RealizationEngine


class CLI(object):

	def __init__(self, command):
		self.parser = argparse.ArgumentParser(prog='rcamp', description='CAMP Realization Tool')
		self.parser.add_argument('command', nargs=1, help='command to start realization', choices=['realize'])
		self.parser.add_argument('model', nargs=1, help='path to file with with model to realize')
		self.parsed_args = self.parser.parse_args(command)


	def execute(self):
		d = vars(self.parsed_args)
		print d

		model_path = d.get('model')[0]

		real_engine = RealizationEngine()
		products = real_engine.get_products(model_path)
		for product in products:
			real_engine.realize_product()
