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

from camp.commands import Command, ShowVersions



class OptionsAreAccepted(TestCase):


    def test_given_the_shortcut(self):
        command_line = "-v"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, ShowVersions)


    def test_given_working_directory(self):
        command_line = "--version"

        command = Command.extract_from(command_line.split())

        self.assertIsInstance(command, ShowVersions)
