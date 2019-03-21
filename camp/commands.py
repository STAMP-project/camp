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
            "-s",
            "--simulated",
            action="store_true",
            dest="is_simulated",
            help="Display but do NOT execute the commands that CAMP triggers")
        execute.add_argument(
            "-t",
            "--test-with",
            dest="testing_tool",
            help="Select the technology used to run the test")
        execute.add_argument(
            "-c",
            "--component",
            dest="component",
            help="Select the component that hosts the tests")

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
                           namespace.testing_tool,
                           namespace.component,
                           namespace.is_simulated)

        else:
            message = "The command '%s' is not yet implemented." % namespace.command
            raise NotImplementedError(message)


    def send_to(self, camp):
        message = "The method '{}.Command#send_to' should have been implemented!"
        raise NotImplementedError(message.format(__name__))



class Generate(Command):
    """
    Encapsulate calls to 'camp generate ...'
    """

    DEFAULT_WORKING_DIRECTORY = "temp/xwiki"
    DEFAULT_COVERAGE = True

    def __init__(self, working_directory=None, coverage=None):
        super(Generate, self).__init__()
        self._working_directory = working_directory or \
                                  self.DEFAULT_WORKING_DIRECTORY
        self._coverage = coverage \
                         if coverage is not None else self.DEFAULT_COVERAGE


    @property
    def working_directory(self):
        return self._working_directory


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
        super(Realize, self).__init__()
        self._working_directory = working_directory or \
                                  self.DEFAULT_WORKING_DIRECTORY
        self._output_directory = output_directory or \
                                 self.DEFAULT_OUTPUT_DIRECTORY

    DEFAULT_WORKING_DIRECTORY = "/temp/"

    DEFAULT_OUTPUT_DIRECTORY = "/temp/out"


    @property
    def working_directory(self):
        return self._working_directory


    @property
    def output_directory(self):
        return self._output_directory


    def send_to(self, camp):
        camp.realize(self)



class Execute(Command):
    """
    Encapsulate calls to 'camp execute ...'
    """

    DEFAULT_WORKING_DIRECTORY = "temp/xwiki"
    DEFAULT_TESTING_TOOL = "maven"
    DEFAULT_COMPONENT = "test"
    DEFAULT_IS_SIMULATED = False


    def __init__(self,
                 working_directory=None,
                 testing_tool=None,
                 component=None,
                 is_simulated=None):
        super(Execute, self).__init__()
        self._working_directory = working_directory or self.DEFAULT_WORKING_DIRECTORY
        self._component = component or self.DEFAULT_COMPONENT
        self._testing_tool = testing_tool or self.DEFAULT_TESTING_TOOL
        self._is_simulated = is_simulated or self.DEFAULT_IS_SIMULATED


    @property
    def working_directory(self):
        return self._working_directory


    @property
    def component(self):
        return self._component


    @property
    def testing_tool(self):
        return self._testing_tool


    @property
    def is_simulated(self):
        return self._is_simulated


    def send_to(self, camp):
        camp.execute(self)
