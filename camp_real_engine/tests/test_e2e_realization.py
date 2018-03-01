import os
import unittest
import shutil

from camp_real_engine.engine import RealizationEngine

class TestE2ERealization(unittest.TestCase):

	def setUp(self):
		self.src_dockerimage = "camp_real_engine/tests/resources/simple_e2e_regexp/Dockerfile"
		self.sub_first_sub = "camp_real_engine/tests/resources/simple_e2e_regexp/exp/Dockerfile_subst1"
		self.sub_second_sub = "camp_real_engine/tests/resources/simple_e2e_regexp/exp/Dockerfile_subst1_2"
		self.src_realmodel = "camp_real_engine/tests/resources/simple_e2e_regexp/test_realmodel.yaml"

		self.src_prodmodel = "camp_real_engine/tests/resources/simple_e2e_regexp/resolmodel.yaml"

		self.tmp_dir = "camp_real_engine/tests/resources/simple_e2e_regexp/tmp"
		self.prod1_dir = os.path.join(self.tmp_dir, 'product1')
		self.prod2_dir = os.path.join(self.tmp_dir, 'product2')

		self.prod1_image_path = os.path.join(self.prod1_dir, 'images')
		self.prod2_image_path = os.path.join(self.prod2_dir, 'images')

		with open(self.sub_first_sub, 'r') as file:
			self.exp_dockerfile_1_subst = file.read()

		with open(self.sub_second_sub, 'r') as file:
			self.exp_dockerfile_1_2_subst = file.read()

		if os.path.exists(self.tmp_dir):
			shutil.rmtree(self.tmp_dir)

		os.makedirs(self.prod1_image_path)
		os.makedirs(self.prod2_image_path)

		shutil.copy(self.src_dockerimage, self.prod1_image_path)
		shutil.copy(self.src_dockerimage, self.prod2_image_path)
		shutil.copy(self.src_realmodel, self.tmp_dir)


	def tearDown(self):
		if os.path.exists(self.tmp_dir):
			shutil.rmtree(self.tmp_dir)


	def test_e2e_realization(self):
		engine = RealizationEngine()
		products = engine.get_products(self.src_prodmodel)

		self.assertIsNotNone(products)
		self.assertEqual(len(products), 2)

		engine.realize_product(products[0])

		tmp_dockerfile = os.path.join(self.prod1_image_path, 'Dockerfile')
		dockerfile_content = ''
		with open(tmp_dockerfile, 'r') as file:
			dockerfile_content = file.read()
		self.assertEqual(dockerfile_content, self.exp_dockerfile_1_2_subst)

		engine.realize_product(products[1])

		tmp_dockerfile = os.path.join(self.prod2_image_path, 'Dockerfile')
		dockerfile_content = ''
		with open(tmp_dockerfile, 'r') as file:
			dockerfile_content = file.read()
		self.assertEqual(dockerfile_content, self.exp_dockerfile_1_2_subst)
