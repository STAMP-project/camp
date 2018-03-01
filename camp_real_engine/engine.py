import yaml

from camp_real_engine.plugins.regexp import RegExp
from camp_real_engine.plugins.model.product import YamlProductModelParser
from camp_real_engine.plugins.model.realization import YamlRealizationModel
from camp_real_engine.plugins.dao.daos import FileContentCommiter


class RealizationEngine(object):

	def get_products(self, file_path):

		content = ""
		with open(file_path, 'r') as file:
			content = file.read()

		yaml_obj = yaml.load(content)
		yaml_parser = YamlProductModelParser()
		product_root = yaml_parser.parse(yaml_obj)
		return product_root.get_products()

	def realize_product(self, product):
		prod_dir = product.get_prod_dir()
		real_path = product.get_prod_real().get_real_path()
		variables = product.get_prod_real().get_prod_vars()

		if not variables or not len(variables):
			print "cannot find any variables to realize product for " + product.get_prod_name()
			return

		content = ""
		with open(real_path, 'r') as file:
			content = file.read()

		yaml_obj = yaml.load(content)
		real_model = YamlRealizationModel()
		real_model.parse(yaml_obj)

		dao = FileContentCommiter(search_dir = prod_dir)
		regexp = RegExp(_content_commiter = dao)
		for variable in variables:
			var_val = (variable.get_var_name(), variable.get_var_value())
			subs = real_model.get_subst_by_var_val(var_val)
			if not subs or not len(subs):
				print "cannot find any substitutions for " + str(var_val)
				continue

			for sub in subs:
				regexp.exe_subst(sub)




	