import yaml
import unittest

from camp_real_engine.model.product import YamlProductModelParser, YamlProductModelBuilder

class TestProductRealModel(unittest.TestCase):

	def setUp(self):
		self.product_model_str = '''
products:
  - product1:
      product_dir: "tests/resources/simple_e2e_regexp/tmp/product1"
      realization:
        path: "tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml"
        variables:
          - variable1: value1
          - variable1: value2
  - product2:
      product_dir: "tests/resources/simple_e2e_regexp/tmp/product2"
      realization:
        path: "tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml"
        variables:
          - variable1: value1
          - variable1: value2
'''

	def test_product_model(self):
		yaml_obj = yaml.load(self.product_model_str)
		builder = YamlProductModelParser()
		product_root = builder.parse(yaml_obj)

		products = product_root.get_products()
		self.assertIsNotNone(products)
		self.assertEqual(len(products), 2)

		product1, product2 = products[0], products[1]
		self.assertEqual(product1.get_prod_name(), "product1")
		self.assertEqual(product2.get_prod_name(), "product2")

		self.assertEqual(product1.get_prod_dir(), "tests/resources/simple_e2e_regexp/tmp/product1")
		self.assertEqual(product2.get_prod_dir(), "tests/resources/simple_e2e_regexp/tmp/product2")

		realization = product1.get_prod_real()
		self.assertEqual(realization.get_real_path(), "tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml")

		variables = realization.get_prod_vars()
		self.assertEqual(len(variables), 2)

		variable1, variable2 = variables[0], variables[1]
		self.assertEqual(variable1.get_var_name(), "variable1")
		self.assertEqual(variable1.get_var_value(), "value1")
		self.assertEqual(variable2.get_var_name(), "variable1")
		self.assertEqual(variable2.get_var_value(), "value2")

		realization = product2.get_prod_real()
		self.assertEqual(realization.get_real_path(), "tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml")

		variables = realization.get_prod_vars()
		self.assertEqual(len(variables), 2)

		variable1, variable2 = variables[0], variables[1]
		self.assertEqual(variable1.get_var_name(), "variable1")
		self.assertEqual(variable1.get_var_value(), "value1")
		self.assertEqual(variable2.get_var_name(), "variable1")
		self.assertEqual(variable2.get_var_value(), "value2")


	def test_poduct_model_ser(self):
		yaml_obj = yaml.load(self.product_model_str)
		parser = YamlProductModelParser()
		product_root = parser.parse(yaml_obj)

		builder = YamlProductModelBuilder()
		yaml_dict = builder.build(product_root)
		actual_str = builder.print_element(yaml_dict)

		exp_str = yaml.dump(yaml_obj, default_flow_style=False)

		self.assertEqual(exp_str, actual_str)