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



class Arguments(object):
    """
    Capture the arguments given through the command line.
    """

    DEFAULT_WORKING_DIRECTORY = "temp/xwiki"


    @staticmethod
    def extract_from(command_line):
        parser = ArgumentParser(prog="CAMP")
        subparsers = parser.add_subparsers()
        generate = subparsers.add_parser(
            "generate",
            help="Generate new test configurations")
        generate.add_argument(
            "-d",
            "--directory",
            help="the directory that contains input files")

        options = parser.parse_args(command_line)

        return Arguments(working_directory=options.directory)


    def __init__(self, working_directory):
        self._working_directory = working_directory or self.DEFAULT_WORKING_DIRECTORY


    @property
    def working_directory(self):
        return self._working_directory
