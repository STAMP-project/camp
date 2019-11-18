#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from argparse import ArgumentParser

from camp import About



class Command(object):

    @staticmethod
    def extract_from(command_line):
        parser = ArgumentParser(prog=About.PROGRAM,
                                description=About.DESCRIPTION)

        parser.add_argument("-v",
                            "--version",
                            dest="command",
                            action="store_const",
                            const="show_version",
                            help="Show the versions of CAMP and its dependencies")

        subparsers = parser.add_subparsers(dest="command")

        generate = subparsers.add_parser(
            "generate",
            help="Generate new test configurations")
        generate.add_argument(
            "-d",
            "--directory",
            dest="working_directory",
            help="the directory that contains input files")
        generate.add_argument(
            "-a",
            "--all",
            action="store_false",
            dest="coverage",
            help="Generate  all possibles configurations")
        generate.add_argument(
            "-c",
            "--coverage",
            action="store_true",
            dest="coverage",
            help="Generate only enough configurations to cover every single variations")

        realize = subparsers.add_parser(
            "realize",
            help="Realize the variables in the test configurations")
        realize.add_argument(
            "-d",
            "--directory",
            dest="working_directory",
            help="the directory that contains the input files")
        realize.add_argument(
            "-o",
            "--output",
            dest="output_directory",
            help="the directory that contains the generated configurations")

        execute = subparsers.add_parser(
            "execute",
            help="Execute the test configurations generated")
        execute.add_argument(
            "-d",
            "--directory",
            dest="working_directory",
            help="the directory that contains the input files")
        execute.add_argument(
            "-i",
            "--include",
            dest="included",
            nargs='+',
            type=int,
            help="Set the indexes of the configurations to execute")
        execute.add_argument(
            "-s",
            "--simulated",
            action="store_true",
            dest="is_simulated",
            help="Display but do NOT execute the commands that CAMP triggers")
        execute.add_argument(
            "-r",
            "--retry",
            type=int,
            dest="retry_count",
            help="Set the maximum number of attempt for the liveness tests")
        execute.add_argument(
            "-y",
            "--retry-delay",
            type=str,
            dest="retry_delay",
            help="Set how long to wait before to run another liveness test")
        execute.add_argument(
            "-l",
            "--logs",
            type=str,
            dest="logs_path",
            help=("Set the relative path where CAMP saves the Docker logs of "
                  "each configuration. By default, the logs of the n-th "
                  "configuration are saved into 'out/config_N/'."))

        values = parser.parse_args(command_line)
        return Command.from_namespace(values)


    @staticmethod
    def from_namespace(namespace):
        if namespace.command == "generate":
            return Generate(namespace.working_directory,
                            namespace.coverage)

        elif namespace.command == "realize":
            return Realize(namespace.working_directory,
                           namespace.output_directory)

        elif namespace.command == "execute":
            return Execute(namespace.working_directory,
                           namespace.is_simulated,
                           namespace.included,
                           namespace.retry_count,
                           namespace.retry_delay,
                           namespace.logs_path)

        elif namespace.command == "show_version":
            return ShowVersions()

        else:
            message = "The command '%s' is not yet implemented." % namespace.command
            raise NotImplementedError(message)


    DEFAULT_WORKING_DIRECTORY = "."

    def __init__(self, working_directory):
        self._working_directory = working_directory \
                                  or self.DEFAULT_WORKING_DIRECTORY


    @property
    def working_directory(self):
        return self._working_directory


    def send_to(self, camp):
        message = "The method '{}.Command#send_to' should have been implemented!"
        raise NotImplementedError(message.format(__name__))



class Generate(Command):
    """
    Encapsulate calls to 'camp generate ...'
    """


    DEFAULT_COVERAGE = True

    def __init__(self, working_directory=None, coverage=None):
        super(Generate, self).__init__(working_directory)
        self._coverage = coverage \
                         if coverage is not None else self.DEFAULT_COVERAGE


    @property
    def only_coverage(self):
        return self._coverage


    def send_to(self, camp):
        camp.generate(self)



class Realize(Command):
    """
    Encapsulate calls to 'camp realize ...'
    """

    def __init__(self, working_directory, output_directory):
        super(Realize, self).__init__(working_directory)
        self._output_directory = output_directory or \
                                 self.DEFAULT_OUTPUT_DIRECTORY

    DEFAULT_OUTPUT_DIRECTORY = "./out"

    @property
    def output_directory(self):
        return self._output_directory


    def send_to(self, camp):
        camp.realize(self)



class Execute(Command):
    """
    Encapsulate calls to 'camp execute ...'
    """

    DEFAULT_IS_SIMULATED = False
    DEFAULT_INCLUDED = []
    DEFAULT_RETRY_COUNT = 5
    DEFAULT_RETRY_DELAY = "30s"
    DEFAULT_LOGS_PATH = ""

    def __init__(self,
                 working_directory=None,
                 is_simulated=None,
                 included=None,
                 max_retries=None,
                 wait_for=None,
                 logs_path=None):
        super(Execute, self).__init__(working_directory)
        self._is_simulated = is_simulated or self.DEFAULT_IS_SIMULATED
        self._included = included or self.DEFAULT_INCLUDED
        self._max_retries = max_retries or self.DEFAULT_RETRY_COUNT
        self._wait_for = wait_for or self.DEFAULT_RETRY_DELAY
        self._logs_path = logs_path or self.DEFAULT_LOGS_PATH


    @property
    def is_simulated(self):
        return self._is_simulated


    @property
    def included_configurations(self):
        return self._included


    @property
    def retry_delay(self):
        return self._wait_for


    @property
    def retry_count(self):
        return self._max_retries


    @property
    def logs_path(self):
        return self._logs_path


    def send_to(self, camp):
        camp.execute(self)



class ShowVersions(Command):


    def __init__(self):
        super(ShowVersions, self).__init__(None)


    def send_to(self, camp):
        camp.show_versions()
