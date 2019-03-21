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

from camp.commands import Command, Execute



class LongOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command_line = "execute --directory my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_with_the_simulation_option(self):
        command_line = ["execute", "--simulate"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(True,
                         command.is_simulated)


    def test_with_a_testing_technology(self):
        command_line = ["execute", "--test-with", "maven"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("maven",
                         command.testing_tool)


    def test_with_a_target_component(self):
        command_line = ["execute", "--component", "foo"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("foo",
                         command.component)



class ShortOptionsAreAccepted(TestCase):

    def test_given_working_directory(self):
        command_line = "execute -d my/test/directory"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_with_the_simulation_option(self):
        command_line = ["execute", "-s"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(True,
                         command.is_simulated)


    def test_with_a_testing_technology(self):
        command_line = ["execute", "--t", "maven"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("maven",
                         command.testing_tool)


    def test_with_a_target_component(self):
        command_line = ["execute", "-c", "foo"]

        command = Command.extract_from(command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual("foo",
                         command.component)


class DefaultValuesAreCorrect(TestCase):

    def setUp(self):
        self._command_line = ["execute"]


    def test_given_working_directory(self):
        command = Command.extract_from(self._command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.working_directory,
                         Execute.DEFAULT_WORKING_DIRECTORY)


    def test_with_the_simulation_option(self):
        command = Command.extract_from(self._command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_IS_SIMULATED,
                         command.is_simulated)


    def test_when_no_argument_is_given(self):
        command = Command.extract_from(self._command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_IS_SIMULATED,
                         command.is_simulated)


    def test_with_a_testing_technology(self):
        command = Command.extract_from(self._command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_TESTING_TOOL,
                         command.testing_tool)


    def test_with_a_target_component(self):
        command = Command.extract_from(self._command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_COMPONENT,
                         command.component)
