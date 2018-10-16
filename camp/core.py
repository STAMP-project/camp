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



class Camp(object):


    def __init__(self, sfinder, sbuilder, ofinder, obuilder):
        self._stack_finder = sfinder
        self._stack_builder = sbuilder
        self._orchestration_finder = ofinder
        self._orchestration_builder = obuilder


    def generate(self, arguments):
        self._prepare_working_directory(arguments)
        self._stack_finder.find(arguments.working_directory)
        self._stack_builder.build()
        self._orchestration_finder.find(arguments.working_directory)
        self._orchestration_builder.build(arguments.working_directory)


    @staticmethod
    def _prepare_working_directory(arguments):
        Camp._create_subdirectory(arguments, "out")
        Camp._create_subdirectory(arguments, "build")


    @staticmethod
    def _create_subdirectory(arguments, subdirectory):
        path = join(arguments.working_directory, subdirectory)
        if not isdir(path):
            makedirs(path)


    def realize(self, arguments):
        pass
