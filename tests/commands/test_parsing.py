#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from unittest import TestCase

from camp.commands import Command, Generate, Realize, Execute



class GenerateTest(TestCase):


    def test_with_default_working_directory(self):
        command_line = ["generate"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         Generate.DEFAULT_WORKING_DIRECTORY)


    def test_with_working_directory(self):
        command_line = ["generate", "-d", "my_directory"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory, "my_directory")



class RealizeTest(TestCase):

    def test_with_defaults(self):
        command_line = ["realize"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Realize)


    def test_with_a_given_resolution_model(self):
        command_line = ["realize", "-p", "my_model.yml"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Realize)
        self.assertEqual("my_model.yml", command.products_file)



class ExecuteTest(TestCase):

    def test_extract_the_given_configuration_file(self):
        command_line = ["execute", "-c", "config.yml"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("config.yml",
                         command.configuration_file) 

    def test_use_default_when_nothing_is_given(self):
        command_line = ["execute"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_CONFIGURATION_FILE,
                         command.configuration_file) 
        
