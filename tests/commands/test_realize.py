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

from camp.commands import Command, Realize



class DefaultValuesAreCorrect(TestCase):


    def test_given_no_working_directory(self):
        command_line = "realize -o output"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Realize)
        self.assertEqual(command.working_directory,
                         Realize.DEFAULT_WORKING_DIRECTORY)



    def test_given_no_working_directory(self):
        command_line = "realize -d workspace"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Realize)
        self.assertEqual(command.output_directory,
                         Realize.DEFAULT_OUTPUT_DIRECTORY)



class ShortOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "realize -d my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Realize)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_given_an_output_directory(self):
        command_line = "realize -o output"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Realize)
        self.assertEqual(command.output_directory,
                         "output")



class LongOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "realize --directory my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Realize)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_given_all_configurations(self):
        command_line = "realize --output output"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Realize)
        self.assertEqual(command.output_directory,
                         "output")
