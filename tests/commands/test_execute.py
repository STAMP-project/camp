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

from camp.commands import Command, Execute



class LongOptionsAreAccepted(TestCase):

    def test_given_a_configuration_file(self):
        command_line = ["execute", "--config", "config.yml"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("config.yml",
                         command.configuration_file)


        
class ShortOptionsAreAccepted(TestCase):

    def test_given_a_configuration_file(self):
        command_line = ["execute", "-c", "config.yml"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("config.yml",
                         command.configuration_file)



class DefaultValuesAreCorrect(TestCase):

    def test_when_no_argument_is_given(self):
        command_line = ["execute"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_CONFIGURATION_FILE,
                         command.configuration_file)
