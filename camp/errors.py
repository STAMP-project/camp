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
    def problem(self):
        return self.PROBLEM % self._path

    PROBLEM = "Could not found any configuration in '%s'."


    @property
    def hint(self):
        return self.HINT % self._path

    HINT = "Have you run 'camp generate -d %s' first?"



class MissingModel(Exception):


    def __init__(self, directory, candidates):
        self._candidates = candidates
        self._directory = directory


    @property
    def problem(self):
        return self.PROBLEM % self._directory

    PROBLEM = "Cannot find any model in '%s'."


    @property
    def hint(self):
        candidates = ", ".join(self._candidates)
        return self.HINT % candidates

    HINT = "CAMP looks for one of the following files: %s."
