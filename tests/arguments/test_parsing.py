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

from camp.arguments import Arguments



class ArgumentsTest(TestCase):


    def test_default_working_directory(self):
        command_line = ["generate"]
        arguments = Arguments.extract_from(command_line)
        self.assertEqual(arguments.working_directory,
                         Arguments.DEFAULT_WORKING_DIRECTORY)


    def test_given_working_directory(self):
        command_line = ["generate", "-d", "my_directory"]
        arguments = Arguments.extract_from(command_line)
        self.assertEqual(arguments.working_directory,
                         "my_directory")
