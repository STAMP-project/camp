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

from camp.execute import MavenExecutor, ShellCommandFailed, Shell, SimulatedShell



class TheShellShould(TestCase):

    def setUp(self):
        self._working_directory = "./"
        self._log = StringIO()
        self._shell = Shell(self._log, "./")


    def test_execute_a_given_command(self):
        self._shell.execute("expr 1 + 4")

        expected_log = ("\n"
                        "camp@bash:./$ expr 1 + 4\n"
                        "5\n")
        self.assertEquals(expected_log, self._log.getvalue())


    def test_override_the_initial_file_directory(self):
        self._shell.execute("expr 1 + 4", "./tests")

        expected_log = ("\n"
                        "camp@bash:./tests$ expr 1 + 4\n"
                        "5\n")
        self.assertEquals(expected_log, self._log.getvalue())


    def test_remember_the_initial_working_directory_when_it_has_been_overriden(self):
        self._shell.execute("expr 1 + 4", "./tests")
        self._shell.execute("echo Hello!")

        expected_log = ("\n"
                        "camp@bash:./tests$ expr 1 + 4\n"
                        "5\n"
                        "\n"
                        "camp@bash:./$ echo Hello!\n"
                        "Hello!\n")
        self.assertEquals(expected_log, self._log.getvalue())



    def test_capture_commands_and_outputs_when_executing_shell_commands(self):
        self._shell.execute("echo Hello World!")

        expected_log = ("\n"
                        "camp@bash:./$ echo Hello World!\n"
                        "Hello World!\n")
        self.assertEquals(expected_log, self._log.getvalue())


    def test_append_outputs_of_multiple_commands_in_the_log(self):
        self._shell.execute("echo Hello World!")
        self._shell.execute("expr 1 + 2")
        self._shell.execute("echo -n That's all folks!")

        expected_log = ("\n"
                        "camp@bash:./$ echo Hello World!\n"
                        "Hello World!\n"
                        "\n"
                        "camp@bash:./$ expr 1 + 2\n"
                        "3\n"
                        "\n"
                        "camp@bash:./$ echo -n That's all folks!\n"
                        "That's all folks!")
        self.assertEquals(expected_log, self._log.getvalue())


    def test_raise_exception_when_a_command_fails(self):
        with self.assertRaises(ShellCommandFailed):
            self._shell.execute("cat file_that_does_not_exist")

        expected_log = ("\n"
                        "camp@bash:./$ cat file_that_does_not_exist\n"
                        "cat: file_that_does_not_exist: No such file or directory\n")
        self.assertEquals(expected_log,
                          self._log.getvalue())


    def test_raise_exception_when_a_command_does_not_exist(self):
        with self.assertRaises(ShellCommandFailed):
            self._shell.execute("unknown_exec with dummy parameters")



class TheSimulatedShellShould(TestCase):

    def setUp(self):
        self._working_directory = "./"
        self._log = StringIO()
        self._shell = SimulatedShell(self._log, self._working_directory)


    def test_not_run_any_command(self):
        self._shell.execute("echo Hello World!")

        expected_log = ("\n"
                        "camp@bash:./$ echo Hello World!\n"
                        ">>> This command was only simulated and was not sent to the shell.\n")
        self.assertEquals(expected_log, self._log.getvalue())


    def test_provides_nothing_as_file_content(self):
        with self._shell.open("a_file_that_does_not_exists", "r") as content:
            self.assertEquals("", content.read())



class TheMavenExecutorShould(TestCase):


    def setUp(self):
        self._log = StringIO()
        self._shell = SimulatedShell(self._log, "./")
        self._execute = MavenExecutor(self._shell)

    def test_build_deploy_run_and_collect_test_results(self):
        configurations = [("out/config_1", None),
                          ("out/config_2", None)]
        self._execute(configurations, "whatever")

        self.assertIn("bash build_images.sh", self._log.getvalue())
        self.assertIn("docker-compose up -d", self._log.getvalue())
        self.assertIn("docker-compose exec -it tests mvn test", self._log.getvalue())
