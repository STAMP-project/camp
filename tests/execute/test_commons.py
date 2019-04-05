#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.commons import ShellCommandFailed, Shell, SimulatedShell, \
    Executor, ExecutorListener

from io import BytesIO

from mock import MagicMock, call

from os import makedirs
from os.path import exists, isdir, join as join_paths, basename

from tempfile import gettempdir

from shutil import copytree, rmtree

from unittest import TestCase



class TheShellShould(TestCase):

    def setUp(self):
        self._listener = MagicMock()
        self._working_directory = "./"
        self._log = BytesIO()
        self._shell = Shell(self._log, "./", self._listener)


    @property
    def log(self):
        return self._log.getvalue().decode()


    def test_notify_listener_when_executing_a_command(self):
        self._shell.execute("expr 1 + 5")

        self._listener.on_shell_command\
                      .assert_called_once_with("expr 1 + 5",
                                               self._working_directory)


    def test_execute_a_given_command(self):
        self._shell.execute("expr 1 + 4")

        expected_log = ("\n"
                        "camp@bash:./$ expr 1 + 4\n"
                        "5\n")
        self.assertEquals(expected_log, self.log)


    def test_returns_the_output_of_the_command(self):
        result = self._shell.execute("expr 1 + 4")

        self.assertEquals(result, "5\n")


    def test_override_the_initial_file_directory(self):
        self._shell.execute("expr 1 + 4", "./tests")

        expected_log = ("\n"
                        "camp@bash:./tests$ expr 1 + 4\n"
                        "5\n")
        self.assertEquals(expected_log, self.log)


    def test_remember_the_initial_working_directory_when_it_has_been_overriden(self):
        self._shell.execute("expr 1 + 4", "./tests")
        self._shell.execute("echo Hello!")

        expected_log = ("\n"
                        "camp@bash:./tests$ expr 1 + 4\n"
                        "5\n"
                        "\n"
                        "camp@bash:./$ echo Hello!\n"
                        "Hello!\n")
        self.assertEquals(expected_log, self.log)


    def test_capture_commands_and_outputs_when_executing_shell_commands(self):
        self._shell.execute("echo Hello World!")

        expected_log = ("\n"
                        "camp@bash:./$ echo Hello World!\n"
                        "Hello World!\n")
        self.assertEquals(expected_log, self.log)


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
        self.assertEquals(expected_log, self.log)


    def test_raise_exception_when_a_command_fails(self):
        with self.assertRaises(ShellCommandFailed):
            self._shell.execute("cat file_that_does_not_exist")

        expected_log = ("\n"
                        "camp@bash:./$ cat file_that_does_not_exist\n"
                        "cat: file_that_does_not_exist: No such file or directory\n")
        self.assertEquals(expected_log,
                          self.log)


    def test_raise_exception_when_a_command_does_not_exist(self):
        with self.assertRaises(ShellCommandFailed):
            self._shell.execute("unknown_exec with dummy parameters")


    def test_recursively_find_all_files_with_a_given_extension(self):
        # delete and recreate a temporary directory with some fake XML files
        temp_directory = gettempdir()
        directory = join_paths(temp_directory, "camp", "execute", "shell")
        if isdir(directory):
            rmtree(directory)
        makedirs(directory)
        self._create_file(directory, "report_1.xml", "<useless-content />")
        subdirectory = join_paths(directory, "more")
        makedirs(subdirectory)
        self._create_file(subdirectory, "report_2.xml", "<useless-content />")
        self._create_file(subdirectory, "report_3.xml", "<useless-content />")

        reports = self._shell.find_all_files(".xml", directory)

        self.assertEquals(3, len(reports))


    @staticmethod
    def _create_file(directory, file_name, content):
        path = join_paths(directory, file_name)
        with open(path, "w+") as new_file:
            new_file.write(content)



class TheSimulatedShellShould(TestCase):

    def setUp(self):
        self._working_directory = "./"
        self._log = BytesIO()
        self._shell = SimulatedShell(self._log, self._working_directory)


    @property
    def log(self):
        return self._log.getvalue().decode()


    def test_not_run_any_command(self):
        self._shell.execute("echo Hello World!")

        expected_log = ("\n"
                        "camp@bash:./$ echo Hello World!\n"
                        ">>> This command was only simulated and was not sent to the shell.\n")
        self.assertEquals(expected_log, self.log)


    def test_provides_nothing_as_file_content(self):
        with self._shell.open("a_file_that_does_not_exists", "r") as content:
            self.assertEquals("", content.read())


    def test_find_no_files(self):
        reports = self._shell.find_all_files(".xml", "/tmp/")
        self.assertEquals([], reports)




class TheExecutorShould(TestCase):


    def setUp(self):
        self._listener = MagicMock(ExecutorListener)
        self._execute = Executor(SimulatedShell(BytesIO(), "."),
                                 self._listener)


    def test_notify_listener(self):
        configurations = [("config_1", "useless"),
                          ("config_2", "useless")]

        self._execute(configurations, "whatever")

        expected_calls = []
        for each, _ in configurations:
            expected_calls.append(call.execution_started_for(each))
            expected_calls.append(call.building_images_for(each))
            expected_calls.append(call.starting_services_for(each))
            expected_calls.append(call.running_tests_for(each))
            expected_calls.append(call.collecting_reports_for(each))
            expected_calls.append(call.stopping_services_for(each))

        self._listener.assert_has_calls(expected_calls)
