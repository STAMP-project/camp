import unittest
from mock import patch, MagicMock
from camp_real_engine.cli import CLI
from camp_real_engine.plugins.model.product import ProductNode


class TestCampRealizeCLI(unittest.TestCase):


	@patch("camp_real_engine.cli.RealizationEngine")
	def test_simple_cli(self, mock_RealizationEngine):
		mock_real_engine = mock_RealizationEngine.return_value
		mock_product = MagicMock(ProductNode)
		mock_real_engine.get_products.return_value = [mock_product]
		
		#camp_realize.py realize /dir/some/file.yaml
		command = ['realize', '/dir/some/file.yaml']
		cli = CLI()
		cli.execute(command)

		mock_real_engine.get_products.assert_called_once_with('/dir/some/file.yaml')
		mock_real_engine.realize_product.assert_called_once_with(mock_product)