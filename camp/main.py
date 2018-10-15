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

from camp import About
from camp.arguments import Arguments
from camp.images.generator import Solver



class Runner(object):


    def __init__(self):
        self._image_generator = Solver()
        self._arguments = None


    def start_camp(self, command_line):
        self._arguments = Arguments.extract_from(command_line)
        self._welcome()
        self._prepare_working_directory()
        self._generate()
        self._goodbye()


    def _welcome(self):
        print "%s v%s (%s)" % (About.PROGRAM, About.VERSION, About.LICENSE)
        print About.COPYRIGHT


    def _prepare_working_directory(self):
        self._create_subdirectory("out")
        self._create_subdirectory("build")


    def _create_subdirectory(self, subdirectory):
        path = join(self._arguments.working_directory, subdirectory)
        if not isdir(path):
            makedirs(path)


    def _generate(self):
        self._image_generator.generate(self._arguments.working_directory)


    def _goodbye(self):
        print "That's all folks!"



def start():
    """Entry point of CAMP as a command line tool"""
    runner = Runner()
    runner.start_camp(argv[1:])
