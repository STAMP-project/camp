#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from os import makedirs
from os.path import isdir, join

from sys import argv

from camp import __VERSION__, __COPYRIGHT__, __LICENSE__
from camp.arguments import Arguments
from camp.composegen import generate
from camp.solver.dockerfile import Solver



class Runner(object):


    def __init__(self):
        self._solver = Solver()
        self._arguments = None


    def start_camp(self, command_line):
        self._arguments = Arguments.extract_from(command_line)
        self._say_hello()
        self._prepare_working_directory()
        self._generate()


    def _say_hello(self):
        print "CAMP v%s (%s)" % (__VERSION__, __LICENSE__)
        print __COPYRIGHT__


    def _prepare_working_directory(self):
        self._create_subdirectory("out")
        self._create_subdirectory("build")


    def _create_subdirectory(self, subdirectory):
        path = join(self._arguments.working_directory, subdirectory)
        if not isdir(path):
            makedirs(path)


    def _generate(self):
        self._solver.generate(self._arguments.working_directory)



def start():
    """Entry point of CAMP as a command line tool"""
    runner = Runner()
    runner.start_camp(argv[1:])
