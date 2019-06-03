#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from __future__ import unicode_literals
from __future__ import print_function

from camp.entities.report import TestReport, TestSuite
from camp.execute.reporting.junit import JUnitXMLReader, \
    JUnitXMLElementNotSupported

from camp.execute.reporting.jmeter import JMeterCSVReader, \
    JMeterCSVInvalidReport


from os import listdir
from os.path import isdir, join as join_paths

from re import search

from subprocess import Popen, PIPE



class Shell(object):

    def __init__(self, log, working_directory, listener=None):
        self._log = log
        self._original_working_directory = working_directory
        self._working_directory = working_directory
        self._listener = listener or ShellListener()


    def execute(self, command, working_directory=None, allow_failure=False):
        self._working_directory = working_directory or self._working_directory
        self._listener.on_shell_command(command, self._working_directory)
        self._output_in_logs(command)
        result = self._run_shell(command, allow_failure)
        self._restore_working_directory()
        return result


    def _output_in_logs(self, command):
        text = self.LOG_OUTPUT.format(self._working_directory, command)
        self._log.write(text.encode())

    LOG_OUTPUT = "\ncamp@bash:{0}$ {1}\n"


    def _run_shell(self, command, allow_failure):
        try:
            process = Popen(command.split(),
                            cwd=self._working_directory,
                            stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            self._log.write(stdout)
            self._log.write(stderr)
            if not allow_failure and process.returncode != 0:
                raise ShellCommandFailed(command,
                                         process.returncode,
                                         stdout,
                                         stderr)
            return stdout.decode()

        except OSError as error:
            raise ShellCommandFailed(command, str(error))


    def _restore_working_directory(self):
        self._working_directory = self._original_working_directory


    @staticmethod
    def open(path, mode):
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


    def __init__(self, log, working_directory, listener=None):
        super(SimulatedShell, self).__init__(log, working_directory, listener)


    def _run_shell(self, command, allow_failure):
        self._log.write(self.COMMAND_SIMULATED.encode())
        return ""


    COMMAND_SIMULATED = (">>> This command was only simulated "
                         "and was not sent to the shell.\n")


    def open(self, path, mode):
        return open("/dev/null")


    def find_all_files(self, extension, directory):
        return []



class ShellListener(object):
    """
    Interface for object who wants to reacts to what the Shell is doing.
    See camp.ui
    """

    def on_shell_command(self, command, working_directory):
        pass



class ShellCommandFailed(Exception):

    def __init__(self, command, exit_code, output=None, error=None):
        self._command = command
        self._exit_code = exit_code
        self._output = output
        self._error = error

    @property
    def command(self):
        return self._command

    @property
    def exit_code(self):
        return self._exit_code

    @property
    def output(self):
        return str(self._output, "utf-8")

    @property
    def error(self):
        return str(self._error, "utf-8")

    def __str__(self):
        return "{0} (with code {1}\nOutput:\n{2}".format(self._command,
                                                self._exit_code,
                                                self._output)


class ExecutorListener(object):
    """
    Interface for object listening to an Executor
    See class camp.ui.UI
    """


    def execution_started_for(self, path):
        pass


    def building_images_for(self, path):
        pass


    def starting_services_for(self, configuration):
        pass


    def running_tests_for(self, configuration):
        pass


    def collecting_reports_for(self, configuration):
        pass


    def on_reading_report(self, report):
        pass


    def on_invalid_report(self, report):
        pass


    def stopping_services_for(self, configuration):
        pass



class Engine(object):


    def __init__(self, component, shell, listener=None):
        self._component = component
        self._shell = shell
        self._listener = listener or ExecutorListener()


    def execute(self, configurations):
        test_results = []
        for each_path, _ in configurations:
            try:
                self._listener.execution_started_for(each_path)

                self._listener.building_images_for(each_path)
                self._build_images(each_path)

                self._listener.starting_services_for(each_path)
                self._start_services(each_path)

                self._listener.running_tests_for(each_path)
                self._run_tests(each_path)

                self._listener.collecting_reports_for(each_path)
                results = self._collect_results(each_path)
                test_results.append(results)

            finally:
                self._listener.stopping_services_for(each_path)
                self._stop_services(each_path)

        return test_results


    def _build_images(self, path):
        working_directory = join_paths(path, "images")
        self._shell.execute(self._BUILD_IMAGES, working_directory)

    _BUILD_IMAGES = "bash build_images.sh"


    def _start_services(self, path):
        self._shell.execute(self._START_SERVICES, path)

    _START_SERVICES = "docker-compose up -d"


    def _run_tests(self, path):
        command = self.RUN_TESTS.format(
            component=self._component.name,
            command=self._component.test_settings.test_command)

        # We allow failure because some test commands return non-zero
        # code when tests fail (e.g., mvn test).
        # See Issue #49
        self._shell.execute(command, path, allow_failure=True)


    # We CANNOT use Docker volumes (option -v). If CAMP runs within a
    # container that spawns new containers by sharing the docker
    # deamon of its host (i.e., by mounting '/var/run/docker.sock'),
    # Docker interprets the paths given to mount volumes with respect
    # to the host file system. (See Issue #35)
    RUN_TESTS = ("docker-compose run "
                 # "--user={uid} "
                 # "-v {path}/images/{component}_0/:/{component} "
                 "{component} "
                 "{command}")


    def _collect_results(self, path):
        container = self._fetch_tests_container_id(path)


        docker_cp = self.FETCH_TEST_REPORTS.format(
            container=container.strip(),
            component=self._component.name,
            location=self._component.test_settings.report_location)

        self._shell.execute(docker_cp, path)

        return self._parse_test_reports(path)


    def _fetch_tests_container_id(self, path):
        docker_ps = self.GET_CONTAINER_ID.format(
            configuration=search(r"(config_[0-9]+)\/?$", path).group(1),
            component=self._component.name)
        return self._shell.execute(docker_ps, path)


    GET_CONTAINER_ID = ("docker ps --all --quiet "
                        "--filter name={configuration}_{component}_run_1")


    FETCH_TEST_REPORTS=("docker cp "
                        "{container}:/{component}/{location} "
                        "./test-reports")


    def _parse_test_reports(self, path):
        all_tests = []

        reader = select_reader_for(
            self._component.test_settings.report_format)

        directory = join_paths(path, "test-reports")
        test_reports = self._shell.find_all_files(
            self._component.test_settings.report_pattern,
            directory)

        for each_report in test_reports:
            try:
                self._listener.on_reading_report(each_report)
                with open(each_report, "r") as report:
                    file_content = report.read()
                    test_suite = reader._extract_from_text(file_content)
                    all_tests.append(test_suite)

            # TODO: This is too general an exception. It relates to a
            # specific reader
            except JUnitXMLElementNotSupported as error:
                self._listener.on_invalid_report(error)

        return TestReport(path, TestSuite("all tests", *all_tests))



    def _stop_services(self, path):
        self._shell.execute(self._STOP_SERVICES, path)

    _STOP_SERVICES = "docker-compose down --volumes --rmi all"




def select_reader_for(report_format):
    key = report_format.strip().upper()
    if key in SUPPORTED_REPORT_FORMAT:
        return SUPPORTED_REPORT_FORMAT[key]()
    raise ReportFormatNotSupported(report_format)


SUPPORTED_REPORT_FORMAT = {
    "JUNIT": JUnitXMLReader,
    "JMETER": JMeterCSVReader,
}



class ReportFormatNotSupported(Exception):

    def __init__(self, technology):
        self._technology = technology

    @property
    def technology(self):
        return self._technology


    @property
    def options(self):
        return [ each_name for each_name, _ in SUPPORTED_TECHNOLOGIES ]
