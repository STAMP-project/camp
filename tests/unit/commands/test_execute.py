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



def _parse(text):
    return Command.extract_from(text.split())



class LongOptionsAreAccepted(TestCase):


    def test_given_working_directory(self):
        command = _parse("execute --directory my/test/directory")

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_with_the_simulation_option(self):
        command = _parse("execute --simulate")

        self.assertIsInstance(command, Execute)
        self.assertEqual(True,
                         command.is_simulated)


    def test_with_the_include_option(self):
        command = _parse("execute --include 1 2 3 4")

        self.assertIsInstance(command, Execute)
        self.assertEqual([1, 2, 3, 4],
                         command.included_configurations)


    def test_with_the_maximum_retries_options(self):
        command = _parse("execute --retry 10")

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.retry_count, 10)


    def test_with_the_wait_for_option(self):
        command = _parse("execute --retry-delay 10s")

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.retry_delay, "10s")



class ShortOptionsAreAccepted(TestCase):

    def test_given_working_directory(self):
        command = _parse("execute -d my/test/directory")

        self.assertIsInstance(command, Execute)
        self.assertEqual(command.working_directory,
                         "my/test/directory")


    def test_with_the_simulation_option(self):
        command = _parse("execute -s")

        self.assertIsInstance(command, Execute)
        self.assertEqual(True,
                         command.is_simulated)


    def test_with_the_include_option(self):
        command = _parse("execute -i 1 2 3 4")

        self.assertIsInstance(command, Execute)
        self.assertEqual([1, 2, 3, 4],
                         command.included_configurations)


    def test_with_the_max_retries_option(self):
        command = _parse("execute -r 15")

        self.assertIsInstance(command, Execute)
        self.assertEqual(15,
                         command.retry_count)

    def test_with_the_retry_delay_option(self):
        command = _parse("execute -y 15s")

        self.assertIsInstance(command, Execute)
        self.assertEqual("15s",
                         command.retry_delay)




class DefaultValuesAreCorrect(TestCase):

    def setUp(self):
        self._command_line = "execute"


    def test_given_the_simplest_command(self):
        command = _parse(self._command_line)

        self.assertIsInstance(command, Execute)
        self.assertEqual(Execute.DEFAULT_WORKING_DIRECTORY,
                         command.working_directory)
        self.assertEqual(Execute.DEFAULT_IS_SIMULATED,
                         command.is_simulated)
        self.assertEqual(Execute.DEFAULT_IS_SIMULATED,
                         command.is_simulated)
        self.assertEqual(Execute.DEFAULT_RETRY_COUNT,
                         command.retry_count)
        self.assertEqual(Execute.DEFAULT_RETRY_DELAY,
                         command.retry_delay)
