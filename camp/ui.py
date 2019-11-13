#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from __future__ import print_function

from camp import About

from os.path import basename



class UI(object):
    """
    Print CAMP events on the terminal or on any other given output
    """

    def __init__(self, output=None):
        from sys import stdout
        self._output = output or stdout


    def welcome(self):
        self._print("{program} v{version} ({ipr})",
                    program=About.PROGRAM,
                    version=About.full_version(),
                    ipr=About.LICENSE)
        self._print(About.COPYRIGHT)
        self._print("")


    def show_versions(self, os, python, z3, docker, compose):
        self._print(" - " + os)
        self._print(" - Python " + ".".join(str(each) for each in python))
        self._print(" - Z3 " + z3)
        self._print(" - " + docker)
        self._print(" - " + compose)


    def goodbye(self):
        self._print("\nThat's all folks!")


    def model_loaded(self, path, model):
        self._print("Loaded '{path}'.", path=path)


    def new_configuration(self, index, configuration, path):
        self._print("\n - Config. {index} in '{path}'.",
                    index=index,
                    path=path)
        self._summarize(configuration)


    def no_configuration_generated(self):
        self._print("\nError: No configuration generated! Is the model correct?")


    def configurations_loaded(self, path):
        self._print("Loading configurations from '{path}' ...", path=path)


    def configuration_realized(self, path):
        self._print(" - Built configuration '{path}.", path=path)


    def execution_started_for(self, path):
        self._print("\n - Executing {path}", path=path)


    def building_images_for(self, path):
        self._print("   1. Building images ...")


    def starting_services_for(self, path):
        self._print("   2. Starting Services ...")


    def running_tests_for(self, path):
        self._print("   3. Running tests ...")


    def collecting_reports_for(self, path):
        self._print("   4. Collecting reports ...")


    def stopping_services_for(self, path):
        self._print("   5. Stopping Services ...")


    def on_shell_command(self, command, working_directory):
        self._print(self.SHELL_COMMAND,
                    command=command,
                    directory=working_directory)

    SHELL_COMMAND  = "      $ {command} (from '{directory}')"


    def on_reading_report(self, report):
        self._print("      Reading {report}", report=basename(report))


    def on_invalid_report(self, error):
        self._print("      Error: {error}", error=str(error))


    def invalid_yaml_model(self, error):
        self._print("\nError:")
        self._print(" - There are errors in the CAMP YAML model.")
        self._print("   Please fix the following issue before to proceed:")
        for index, each_warning in enumerate(error.warnings, 1):
            self._print("    {index}. {warning}",
                        index=index,
                        warning=str(each_warning))


    def invalid_model(self, details):
        self._print("\nError:")
        self._print(" - There are errors in the CAMP  model.")
        self._print("   Please fix the following issue before to proceed:")
        for index, each_error in enumerate(details.errors, 1):
            self._print("     {index}. {error}",
                        index=index,
                        error=str(each_error))


    def missing_model(self, error):
        self._print("\nError:")
        self._print(" - Unable to find a CAMP model in '{folder}'.",
                    folder=error.searched_folder)
        file_names = ", ".join(error.searched_files)
        self._print("   CAMP looks for one of the following: {file_names}.",
                    file_names=file_names)


    def no_configuration_found(self, error):
        self._print("\nError:")
        self._print(" - Unable to find any generated configuration  in '{folder}'.",
                    folder=error.searched_folder)
        self._print("   Have you run 'camp generate -d {folder}?",
                    folder=error.searched_folder)

    def no_configuration_with_index(self, index):
        self._print("Warning: No configuration found with index {index}",
                    index=index)


    def invalid_substitution(self, error):
        self._print(self.INVALID_SUBSTITUTION, searched=error.pattern,
                    target=error.target)

    INVALID_SUBSTITUTION=("\n"
                          "Error:\n"
                          "Vain substitution: No match found!'\n"
                          "  - pattern: '{searched}'\n"
                          "  - target file: '{target}'\n"
                          "Is the pattern appropriate? What about the file content?")

    def service_not_ready(self, error):
        self._print("Service is not ready!")
        self._print("All {retry} failed (with {delay} delay in between).",
                    retry=error.retry_count,
                    delay=error.retry_delay)

    def shell_command_failed(self, error):
        self._print("\nTest execution aborted!")
        self._print(" - Error: A shell command failed (code: {code})", code=error.exit_code)
        self._print("   $ {command}", command=error.command)
        self._print("   Check out logs in 'camp_execute.log'.")
        self._print(error.output)
        self._print(error.error)


    def report_format_not_supported(self, error):
        self._print("\nTest execution aborted!")
        self._print(" - Error: Reading '{techno}' reports is not supported.",
                    techno=error.technology)
        self._print("   Options are: {options}", options=error.options)
        self._print("   Is there a newer version of CAMP available?")


    def unexpected_error(self, error, stack_trace):
        self._print("Unexpected error:")
        self._print(" - {0}".format(str(error)))
        self._print("   In file: {0}".format(stack_trace[-1][0]))
        self._print("      {}: {}".format(stack_trace[-1][1], stack_trace[-1][3]))
        self._print("   Please report this at '{issue}'.",
                    issue=self.ISSUE_PAGE)

    ISSUE_PAGE = "https://github.com/STAMP-project/camp/issues"


    def _summarize(self, configuration):
        components = set()
        for each in configuration.instances:
            name = each.definition.name
            if each.configuration:
                name  += " (" +", ".join(str(v) for _,v in each.configuration) + ")"
            components.add(name)
        text = "   Includes " + ', '.join(components)
        self._print(self._head(text, length=75))


    def summarize_execution(self, results):
        self._print("\nTest SUMMARY:")
        self._print("")
        self._print(self._TEST_SUMMARY,
                    config="Configuration",
                    run="RUN",
                    passed="PASS",
                    fail="FAIL",
                    error="ERROR")
        self._print(self._LINE)
        total_run = 0
        total_pass = 0
        total_fail = 0
        total_error = 0
        for each in results:
            self._print(self._TEST_SUMMARY,
                        config=self._tail(each.configuration_name),
                        run=each.run_test_count,
                        passed=each.passed_test_count,
                        fail=each.failed_test_count,
                        error=each.error_test_count)
            total_run += each.run_test_count
            total_pass += each.passed_test_count
            total_fail += each.failed_test_count
            total_error += each.error_test_count
        self._print(self._LINE)
        self._print(self._TEST_SUMMARY,
                    config="TOTAL",
                    run=total_run,
                    passed=total_pass,
                    fail=total_fail,
                    error=total_error)


    _TEST_SUMMARY = "{config:<25} {run:>7}{passed:>7}{fail:>7}{error:>7}"
    _LINE = "-" * 25 + "-" + "-" * (4 * 7 + 1)


    def _print(self, pattern, **values):
        if values:
            self._output.write(pattern.format(**values) + "\n")
        else:
            self._output.write(pattern+ "\n")


    @staticmethod
    def _head(text, length=20):
        if len(text) < 20:
            return text
        return text[0:length] + "..."


    @staticmethod
    def _tail(text, length=20):
        if len(text) < 20:
            return text
        return "..." + text[-length:]
