from camp_real_engine.plugins.abstract.abc_visitor import Visitee

from camp_real_engine.plugins.abstract.abc_prod_data_model import ABCProductRoot, ABCProduct, ABCProductReal
from camp_real_engine.plugins.abstract.abc_prod_data_model import ABCProductVar, ABCProductVisitor, ABCProductRealNode



class ProductRootNode(ABCProductRealNode, ABCProductRoot):
	pass

class ProductNode(ABCProductRealNode, ABCProduct):
	pass

class ProductRealNode(ABCProductRealNode, ABCProductReal):
	pass

class ProductVarNode(ABCProductRealNode, ABCProductVar):
	pass


class ProductComponentFactory(object):

	def creat_product_root(self):
		return ProductRootNode()

	def create_product(self):
		return ProductNode()

	def create_product_real(self):
		return ProductRealNode()

	def create_product_var(self):
		return ProductVarNode()


class YamlProductVisitor(ABCProductVisitor):

	def visit_product_root(self, visitee, **kwargs):
		pass

	def visit_product(self, visitee, **kwargs):
		pass

	def visit_product_real(self, visitee, **kwargs):
		pass

	def visit_product_var(self, visitee, **kwargs):
		pass


class YamlProductPrinterVisitor(ABCProductVisitor):

	def visit_product_root(self, visitee, **kwargs):
		pass

	def visit_product(self, visitee, **kwargs):
		pass

	def visit_product_real(self, visitee, **kwargs):
		pass

	def visit_product_var(self, visitee, **kwargs):
		pass


class YamlProductModelBulder(object):

	def __init__(self, *args, **kwargs):
		self.visitor = YamlProductVisitor()
		self.factory = ProductComponentFactory()

	def parse(self, yaml_obj):
		pass


	def get_products(self):
		pass

