#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from StringIO import StringIO

from unittest import TestCase

from camp.execute import ShellCommand, ShellCommandFailed




class AShellCommand(TestCase):


    def test_execute_the_command(self):
        log = StringIO()
        command = ShellCommand("expr 1 + 1", log)
        command.run()
        self.assertEquals("2\n", log.getvalue())


    def test_capture_its_output(self):
        log = StringIO()
        command = ShellCommand("echo Hello World!", log)
        command.run()
        self.assertEquals("Hello World!\n", log.getvalue())


    def test_raise_exception_when_the_command_fails(self):
        log = StringIO()
        command = ShellCommand("cat file_that_does_not_exist", log)
        with self.assertRaises(ShellCommandFailed):
            command.run()
        self.assertEquals("cat: file_that_does_not_exist: No such file or directory\n",
                          log.getvalue())


    def test_raise_exception_when_command_does_not_exist(self):
        log = StringIO()
        command = ShellCommand("unknown_exec with dummy parameters", log)
        with self.assertRaises(ShellCommandFailed):
            command.run()
