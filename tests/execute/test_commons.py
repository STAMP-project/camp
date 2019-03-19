#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.commons import ShellCommandFailed, Shell, SimulatedShell, FailedTest, \
    ErroneousTest, SuccessfulTest, TestSuite, TestReport

from os import makedirs
from os.path import exists, isdir, join as join_paths, basename

from tempfile import gettempdir

from shutil import copytree, rmtree

from StringIO import StringIO

from unittest import TestCase



class ATestShould(object):

    def setUp(self):
        self._identifier = "Foo Test"

    def test_have_no_child(self):
        self.assertEquals([], self._testcase.children)

    def test_have_run_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.run_test_count)

    def test_expose_their_identifier(self):
        self.assertEquals(self._identifier, self._testcase.identifier)



class ASuccessfulTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._testcase = SuccessfulTest(self._identifier)

    def test_have_failed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.erroneous_test_count)

    def test_have_passed_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.passed_test_count)



class AFailedTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._testcase = FailedTest(self._identifier,
                                    "There was an error")

    def test_have_passed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.passed_test_count)

    def test_have_failed_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.erroneous_test_count)

    def test_expose_its_failure(self):
        self.assertEquals("There was an error",
                          self._testcase.failure)



class AnErroneousTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._testcase = ErroneousTest(self._identifier,
                                       "There was an error")

    def test_have_passed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.passed_test_count)

    def test_have_failed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.erroneous_test_count)

    def test_expose_its_error(self):
        self.assertEquals("There was an error",
                          self._testcase.error)


class ATestSuiteShould(TestCase):

    def setUp(self):
        self._suite = TestSuite("My test suite",
            SuccessfulTest("Test 1"),
            SuccessfulTest("Test 2"),
            FailedTest("Test 3", "failure"),
            ErroneousTest("Test 4", "error"),
            TestSuite("My inner test suite",
                SuccessfulTest("Test 5"),
                SuccessfulTest("Test 6"),
                FailedTest("Test 7", "failure")
        ))

    def test_account_for_all_tests_run(self):
        self.assertEquals(7, self._suite.run_test_count)


    def test_account_for_all_tests_passed(self):
        self.assertEquals(4, self._suite.passed_test_count)


    def test_account_for_all_tests_failed(self):
        self.assertEquals(2, self._suite.failed_test_count)


    def test_account_for_all_erroneous_tests(self):
        self.assertEquals(1, self._suite.erroneous_test_count)



class ATestReportShould(TestCase):


    def setUp(self):
        self._tests = TestSuite("Fake Test Suite",
                                SuccessfulTest("Test 1"),
                                SuccessfulTest("Test 2"),
                                SuccessfulTest("Test 3"),
                                FailedTest("Test 4", "Assertion failed!"),
                                ErroneousTest("Test 5", "Unknown Error"))
        self._report = TestReport("./config", self._tests)


    def test_expose_the_number_of_passed_tests(self):
        self.assertEquals(self._tests.passed_test_count,
                          self._report.passed_test_count)


    def test_expose_the_number_of_failed_tests(self):
        self.assertEquals(self._tests.failed_test_count,
                          self._report.failed_test_count)


    def test_expose_the_number_of_erroneous_tests(self):
        self.assertEquals(self._tests.erroneous_test_count,
                          self._report.error_test_count)

    def test_expose_the_number_of_run_tests(self):
        self.assertEquals(self._tests.run_test_count,
                          self._report.run_test_count)

    def test_expose_the_path_to_related_configuration(self):
        self.assertEquals("./config",
                          self._report.configuration_name)



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


    def test_find_no_files(self):
        reports = self._shell.find_all_files(".xml", "/tmp/")
        self.assertEquals([], reports)
