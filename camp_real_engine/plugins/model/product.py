from camp_real_engine.plugins.abstract.abc_visitor import Visitee

from camp_real_engine.plugins.abstract.abc_prod_data_model import ABCProductRoot, ABCProduct, ABCProductReal
from camp_real_engine.plugins.abstract.abc_prod_data_model import ABCProductVar, ABCProductVisitor, ABCProductRealNode



class ProductRootNode(ABCProductRealNode, ABCProductRoot):
	
	def __init__(self):
		self.products = []

	def append_product(self, prod):
		self.products.append(prod)

	def get_products(self):
		return self.products


class ProductNode(ABCProductRealNode, ABCProduct):
	
	def __init__(self):
		self.prod_name = None
		self.prod_dir = None
		self.real = None

	def set_prod_name(self, _name):
		self.prod_name = _name

	def get_prod_name(self):
		return self.prod_name

	def set_prod_dir(self, _dir):
		self.prod_dir = _dir

	def get_prod_dir(self):
		return self.prod_dir

	def set_prod_real(self, _real):
		self.real = _real

	def get_prod_real(self):
		return self.real


class ProductRealNode(ABCProductRealNode, ABCProductReal):
	
	def __init__(self):
		self.real_path = None
		self.prod_vars = []

	def set_real_path(self, _path):
		self.real_path = _path

	def get_real_path(self):
		return self.real_path

	def append_prod_vars(self, var):
		self.prod_vars.append(var)

	def get_prod_vars(self):
		return self.prod_vars


class ProductVarNode(ABCProductRealNode, ABCProductVar):
	
	def __init__(self):
		self.name = None
		self.value = None

	def set_var_name(self, _name):
		self.name = _name

	def get_var_name(self):
		return self.name

	def set_var_value(self, _value):
		self.value = _value

	def get_var_value(self):
		return self.value


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
		yaml_root = kwargs.get("yaml_obj")

	def visit_product(self, visitee, **kwargs):
		prod_root = kwargs.get("prod_root")
		yaml_prod = kwargs.get("yaml_prod")
		prod_root.append_product(visitee)

		prod_name = yaml_prod.keys()[0]
		prod_dir = yaml_prod.values()[0]['product_dir']
		visitee.set_prod_name(prod_name)

		visitee.set_prod_dir(prod_dir)


	def visit_product_real(self, visitee, **kwargs):
		prod = kwargs.get('prod')
		yaml_real = kwargs.get('yaml_real')

		prod.set_prod_real(visitee)
		visitee.set_real_path(yaml_real['path'])

	def visit_product_var(self, visitee, **kwargs):
		real = kwargs.get("prod_real")
		yaml_var = kwargs.get("yaml_var")

		real.append_prod_vars(visitee)
		visitee.set_var_name(yaml_var.keys()[0])
		visitee.set_var_value(yaml_var.values()[0])


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
		products = yaml_obj['products']
		croot = self.factory.creat_product_root()
		croot.accept(self.visitor, yaml_root = yaml_obj)
		for product in products:
			cprod = self.factory.create_product()
			cprod.accept(self.visitor, prod_root = croot, yaml_prod = product)
			creal = self.factory.create_product_real()
			yaml_realization = product.values()[0]['realization']
			creal.accept(self.visitor, prod = cprod, yaml_real = yaml_realization)
			for variable in yaml_realization['variables']:
				cvar = self.factory.create_product_var()
				cvar.accept(self.visitor, prod_real = creal, yaml_var = variable)
		return croot

