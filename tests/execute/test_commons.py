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

from camp.execute.commons import ShellCommandFailed, Shell, SimulatedShell, FailedTest, \
    ErroneousTest, SuccessfulTest, TestSuite



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
