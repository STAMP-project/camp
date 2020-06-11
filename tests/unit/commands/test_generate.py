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


    def test_given_no_parameters(self):
        command_line = "generate --mode  all"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         Generate.DEFAULT_WORKING_DIRECTORY)



    def test_given_no_working_directory(self):
        command_line = "generate -d my/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.mode,
                         Generate.DEFAULT_MODE)



class ShortOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "generate --d my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_given_covering_mode(self):
        command_line = "generate -m covering"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.mode, Generate.COVERING)


    def test_given_all_configurations_mode(self):
        command_line = "generate -m all"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.mode, Generate.ALL)


    def test_given_atomic_mode(self):
        command_line = "generate -m all"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.mode, Generate.ALL)



class LongOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "generate --directory my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_given_covering_mode(self):
        command_line = "generate --mode covering"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertTrue(command.mode, Generate.COVERING)


    def test_given_atomic_mode(self):
        command_line = "generate --mode atomic"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEquals(command.mode, Generate.ATOMIC)
        

    def test_given_all_configurations_mode(self):
        command_line = "generate --mode all"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Generate)
        self.assertEquals(command.mode, Generate.ALL)
