import yaml
import unittest

from camp_real_engine.plugins.model.product import YamlProductModelBulder

class TestProductRealModel(unittest.TestCase):

	def setUp(self):
		self.product_model_str = '''
products:
  - product1:
      product_dir: "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/product1"
      realization:
        path: "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml"
        variables:
          - variable1: value1
          - variable1: value2
  - product2:
      product_dir: "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/product2"
      realization:
        path: "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml"
        variables:
          - variable1: value1
          - variable1: value2
'''

	def test_product_model(self):
		yaml_obj = yaml.load(self.product_model_str)
		builder = YamlProductModelBulder()
		product_root = builder.parse(yaml_obj)

		products = product_root.get_products()
		self.assertIsNotNone(products)
		self.assertEqual(len(products), 2)

		product1, product2 = products[0], products[1]
		self.assertEqual(product1.get_name(), "product1")
		self.assertEqual(product2.get_name(), "product2")

		self.assertEqual(product1.get_product_dir(), "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/product1")
		self.assertEqual(product2.get_product_dir(), "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/product2")

		realization = product1.get_product_real()
		self.assertEqual(realization.get_real_path(), "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml")

		variables = realization.get_product_vars()
		self.assertEqual(len(variables), 2)

		variable1, variable2 = variables[0], variables[1]
		self.assertEqual(variable1.get_name(), "variable1")
		self.assertEqual(variable1.get_value(), "value1")
		self.assertEqual(variable2.get_name(), "variable1")
		self.assertEqual(variable2.get_value(), "value2")

		realization = product2.get_product_real()
		self.assertEqual(realization.get_real_path(), "camp_real_engine/tests/resources/simple_e2e_regexp/tmp/test_realmodel.yaml")

		variables = realization.get_product_vars()
		self.assertEqual(len(variables), 2)

		variable1, variable2 = variables[0], variables[1]
		self.assertEqual(variable1.get_name(), "variable1")
		self.assertEqual(variable1.get_value(), "value1")
		self.assertEqual(variable2.get_name(), "variable1")
		self.assertEqual(variable2.get_value(), "value2")