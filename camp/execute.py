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



class ShellCommand(object):


    def __init__(self, command, logfile, working_directory=None):
        self._command = command
        self._logfile = logfile
        self._working_directory = working_directory


    def run(self):
        try:
            process = Popen(self._command.split(),
                            cwd=self._working_directory,
                            stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            self._logfile.write(stdout)
            self._logfile.write(stderr)
            if process.returncode != 0:
                raise ShellCommandFailed(self._command)

        except OSError as error:
            raise ShellCommandFailed(self._command)



class SimulatedShellCommand(ShellCommand):

    def __init__(self, command, logfile, directory):
        super(SimulatedShellCommand, self).__init__(command, logfile, directory)


    def run(self):
        print "      $ {0} (from '{1}')".format(self._command, self._working_directory)



class ShellCommandFailed(Exception):

    def __init__(self, command):
        self._command = command



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



class Executor:


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
        log_file_path = join_paths(path, "log_build_images.txt")
        with open(log_file_path, "w+") as log_file:
            command = self._execute(self._BUILD_IMAGES,
                                    log_file,
                                    join_paths(path, "images"))
            command.run()

    _BUILD_IMAGES = "bash build_images.sh"


    def _execute(self, command, log_file, directory):
        return ShellCommand(command, log_file, directory)


    def _start_services(self, path):
        print "   2. Starting Services ..."
        log_file_path = join_paths(path, "log_start_services.txt")
        with open(log_file_path, "w+") as log_file:
            command = self._execute(self._START_SERVICES,
                                    log_file,
                                    path)
            command.run()

    _START_SERVICES = "docker-compose up -d"


    def _run_tests(self, path, command):
        print "   3. Running tests ..."
        log_file_path = join_paths(path, "log_run_tests.txt")
        with open(log_file_path, "w+") as log_file:
            command = self._execute(self._RUN_TESTS + command,
                                    log_file,
                                    path)
            command.run()

    _RUN_TESTS = "docker-compose exec -it tests "


    def _collect_results(self, path):
        return TestResults(path, 3, 3, 4)



class Simulator(Executor):


    def _execute(self, command, log_file, directory):
        return SimulatedShellCommand(command, log_file, directory)

    def _collect_results(self, path):
        return TestResults(path, 0, 0, 0)
