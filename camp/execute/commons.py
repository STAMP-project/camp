#
# CAMP
#
# Copyright (C) 2017 - 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

from os.path import join as join_paths

from subprocess import Popen, PIPE



class Shell(object):

    def __init__(self, log, working_directory):
        self._log = log
        self._original_working_directory = working_directory
        self._working_directory = working_directory


    def execute(self, command, working_directory=None):
        self._working_directory = working_directory or self._working_directory
        self._output_on_console(command)
        self._output_in_logs(command)
        self._run_shell(command)
        self._restore_working_directory()


    def _output_in_logs(self, command):
        text = self.LOG_OUTPUT.format(self._working_directory, command)
        self._log.write(text)

    LOG_OUTPUT = "\ncamp@bash:{0}$ {1}\n"


    def _output_on_console(self, command):
        text = self.CONSOLE_OUTPUT.format(command, self._working_directory)
        print text

    CONSOLE_OUTPUT = "      $ {0} (from '{1}')"


    def _run_shell(self, command):
        try:
            process = Popen(command.split(),
                            cwd=self._working_directory,
                            stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            self._log.write(stdout)
            self._log.write(stderr)
            if process.returncode != 0:
                raise ShellCommandFailed(command)

        except OSError as error:
            raise ShellCommandFailed(command, str(error))


    def _restore_working_directory(self):
        self._working_directory = self._original_working_directory


    def open(self, path, mode):
        return open(path, mode)



class SimulatedShell(Shell):


    def __init__(self, log, working_directory):
        super(SimulatedShell, self).__init__(log, working_directory)


    def _run_shell(self, command):
        self._log.write(self.COMMAND_SIMULATED)


    COMMAND_SIMULATED = (">>> This command was only simulated "
                         "and was not sent to the shell.\n")


    def open(self, path, mode):
        return open("/dev/null")



class ShellCommandFailed(Exception):

    def __init__(self, command, output=None):
        self._command = command
        self._output = output


    def __str__(self):
        return self._output



class TestResults:

    def __init__(self, name, passed, failed, error):
        self._name = name
        self._passed = passed
        self._failed = failed
        self._error = error

    @property
    def configuration_name(self):
        return self._name

    @property
    def failed_test_count(self):
        return self._failed

    @property
    def passed_test_count(self):
        return self._passed

    @property
    def error_test_count(self):
        return self._error

    @property
    def run_test_count(self):
        return self.passed_test_count + \
            self.failed_test_count + \
            self.error_test_count


class Verdict:
    PASS = 1
    FAIL = 2
    ERROR = 3


class Test(object):

    def __init__(self, identifier, verdict):
        self._identifier = identifier
        self._verdict = verdict

    @property
    def identifier(self):
        return self._identifier


    @property
    def children(self):
        return []


    @property
    def run_test_count(self):
        return 1


    @property
    def passed_test_count(self):
        return 1 if self._verdict == Verdict.PASS \
            else 0


    @property
    def failed_test_count(self):
        return 1 if self._verdict == Verdict.FAIL \
            else 0


    @property
    def erroneous_test_count(self):
        return 1 if self._verdict == Verdict.ERROR \
            else 0


class SuccessfulTest(Test):

    def __init__(self, identifier):
        super(SuccessfulTest, self).__init__(identifier, Verdict.PASS)



class FailedTest(Test):

    def __init__(self, identifier, failure):
        super(FailedTest, self).__init__(identifier, Verdict.FAIL)
        self._failure = failure


    @property
    def failure(self):
        return self._failure



class ErroneousTest(Test):

    def __init__(self, identifier, error):
        super(ErroneousTest, self).__init__(identifier, Verdict.ERROR)
        self._error = error


    @property
    def error(self):
        return self._error



class TestSuite(Test):

    def __init__(self, identifier, *tests):
        super(TestSuite, self).__init__(identifier, None)
        self._tests = tests

    @Test.run_test_count.getter
    def run_test_count(self):
        return sum(each.run_test_count for each in self._tests)

    @Test.passed_test_count.getter
    def passed_test_count(self):
        return sum(each.passed_test_count for each in self._tests)

    @Test.failed_test_count.getter
    def failed_test_count(self):
        return sum(each.failed_test_count for each in self._tests)

    @Test.erroneous_test_count.getter
    def erroneous_test_count(self):
        return sum(each.erroneous_test_count for each in self._tests)



class Executor(object):


    def __init__(self, shell):
        self._shell = shell


    def __call__(self, configurations, command="whatever"):
        test_results = []
        for each_path, _ in configurations:
            print " - Executing ", each_path
            try:
                self._build_images(each_path)
                self._start_services(each_path)
                self._run_tests(each_path, command)
                results = self._collect_results(each_path)

            except ShellCommandFailed as error:
                results = TestResults(path, -1, -1, -1)

            test_results.append(results)

        return test_results


    def _build_images(self, path):
        print "   1. Building images ..."
        working_directory = join_paths(path, "images")
        self._shell.execute(self._BUILD_IMAGES, working_directory)

    _BUILD_IMAGES = "bash build_images.sh"


    def _start_services(self, path):
        print "   2. Starting Services ..."
        self._shell.execute(self._START_SERVICES, path)

    _START_SERVICES = "docker-compose up -d"


    def _run_tests(self, path, command):
        print "   3. Running tests ..."
        self._shell.execute(self._RUN_TESTS + command, path)

    _RUN_TESTS = "docker-compose exec -it tests "


    def _collect_results(self, path):
        return TestResults(path, 3, 3, 4)
