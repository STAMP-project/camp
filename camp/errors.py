#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



class NoConfigurationFound(Exception):


    def __init__(self, path):
        self._path = path


    @property
    def searched_folder(self):
        return self._path



class MissingModel(Exception):


    def __init__(self, directory, candidates):
        self._candidates = candidates
        self._folder = directory


    @property
    def searched_folder(self):
        return self._folder

    @property
    def searched_files(self):
        return self._candidates
