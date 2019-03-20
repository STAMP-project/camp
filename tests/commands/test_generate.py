#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from unittest import TestCase

from camp.commands import Command, Generate



class DefaultValuesAreCorrect(TestCase):


    def test_given_no_working_directory(self):
        command_line = "generate --all"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         Generate.DEFAULT_WORKING_DIRECTORY)



    def test_given_no_working_directory(self):
        command_line = "generate -d my/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.only_coverage,
                         Generate.DEFAULT_COVERAGE)



class ShortOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "generate --d my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_given_only_coverage(self):
        command_line = "generate --c"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertTrue(command.only_coverage)


    def test_given_all_configurations(self):
        command_line = "generate --a"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertFalse(command.only_coverage)



class LongOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "generate --directory my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_given_only_coverage(self):
        command_line = "generate --coverage"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertTrue(command.only_coverage)


    def test_given_all_configurations(self):
        command_line = "generate --all"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertFalse(command.only_coverage)
