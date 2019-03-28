#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from os import listdir
from os.path import isdir, join as join_paths

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
        result = self._run_shell(command)
        self._restore_working_directory()
        return result

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
                raise ShellCommandFailed(command,
                                         process.returncode)
            return stdout

        except OSError as error:
            raise ShellCommandFailed(command, str(error))


    def _restore_working_directory(self):
        self._working_directory = self._original_working_directory


    def open(self, path, mode):
        return open(path, mode)


    def find_all_files(self, extension, directory):
        found_files = []
        for any_file in listdir(directory):
            path = join_paths(directory, any_file)
            if isdir(path):
                found_files.extend(self.find_all_files(extension, path))
            else:
                if any_file.endswith(extension):
                    found_files.append(path)
        return found_files



class SimulatedShell(Shell):


    def __init__(self, log, working_directory):
        super(SimulatedShell, self).__init__(log, working_directory)


    def _run_shell(self, command):
        self._log.write(self.COMMAND_SIMULATED)
        return ""


    COMMAND_SIMULATED = (">>> This command was only simulated "
                         "and was not sent to the shell.\n")


    def open(self, path, mode):
        return open("/dev/null")


    def find_all_files(self, extension, directory):
        return []



class ShellCommandFailed(Exception):

    def __init__(self, command, exit_code, output=None):
        self._command = command
        self._exit_code = exit_code
        self._output = output

    @property
    def command(self):
        return self._command

    @property
    def exit_code(self):
        return self._exit_code

    def __str__(self):
        return "{0} (with code {1}\nOutput:\n{2}".format(self._command,
                                                self._exit_code,
                                                self._output)



class Executor(object):


    def __init__(self, shell):
        self._shell = shell


    def __call__(self, configurations, component):
        test_results = []
        for each_path, _ in configurations:
            print "\n - Executing ", each_path
            self._build_images(each_path)
            self._start_services(each_path)
            self._run_tests(each_path, component)
            results = self._collect_results(each_path, component)
            test_results.append(results)
            self._stop_services(each_path)

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
        return TestReport(path)


    def _stop_services(self, path):
        print "   5. Stopping Services ..."
        self._shell.execute(self._STOP_SERVICES, path)

    _STOP_SERVICES = "docker-compose down"
