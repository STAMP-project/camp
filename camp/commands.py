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
            "-p",
            "--products",
            dest="products",
            help="the file that describes the products to realize")
            

        values = parser.parse_args(command_line)
        return Command.from_namespace(values)


    @staticmethod
    def from_namespace(namespace):
        if namespace.command == "generate":
            return Generate(namespace.working_directory)
        elif namespace.command == "realize":
            return Realize(namespace.products)
        else:
            message = "The command '%s' is not yet implemented." % namespace.command
            raise NotImplementedError(message)


    def send_to(self, camp):
        pass



class Generate(Command):
    """
    Encapsulate ca call to 'camp generate'
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
    Encapsulate a call to 'camp realize'
    """

    def __init__(self, products_file):
        self._products_file = products_file


    @property
    def products_file(self):
        return self._products_file
    
    def send_to(self, camp):
        camp.realize(self)

