#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
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

        realize = subparsers.add_parser(
            "realize",
            help="Realize the variables in the test configurations")
        realize.add_argument(
            "-d",
            "--directory",
            dest="working_directory",
            help="the directory that describes that contains the input files")
        realize.add_argument(
            "-o",
            "--output",
            dest="output_directory",
            help="the directory that contains the generated configurations")

        execute = subparsers.add_parser(
            "execute",
            help="Execute the test configurations generated")
        execute.add_argument(
            "-c",
            "--config",
            dest="configuration_file",
            help="The INI file that describes which configurations to execute")

        values = parser.parse_args(command_line)
        return Command.from_namespace(values)


    @staticmethod
    def from_namespace(namespace):
        if namespace.command == "generate":
            return Generate(namespace.working_directory)

        elif namespace.command == "realize":
            return Realize(namespace.working_directory,
                           namespace.output_directory)

        elif namespace.command == "execute":
            return Execute(namespace.configuration_file)

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

    def __init__(self, working_directory):
        self._working_directory = working_directory or \
                                  self.DEFAULT_WORKING_DIRECTORY


    @property
    def working_directory(self):
        return self._working_directory


    def send_to(self, camp):
        camp.generate(self)



class Realize(Command):
    """
    Encapsulate calls to 'camp realize ...'
    """

    def __init__(self, working_directory, output_directory):
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


    DEFAULT_CONFIGURATION_FILE = "config.ini"


    def __init__(self, configuration_file):
        super(Command, self).__init__()
        self._configuration_file = configuration_file \
                                   or self.DEFAULT_CONFIGURATION_FILE


    @property
    def configuration_file(self):
        return self._configuration_file


    def send_to(self, camp):
        camp.execute(self)
