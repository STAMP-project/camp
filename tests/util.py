#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from __future__ import unicode_literals

from os import makedirs
from os.path import isdir, join as join_paths

from shutil import rmtree

from tempfile import mkdtemp



def create_temporary_workspace(location):
    temporary_directory = mkdtemp(prefix=CAMP_PREFIX)
    workspace = join_paths(temporary_directory, location)
    if isdir(workspace):
        rmtree(workspace)
    makedirs(workspace)
    return workspace


CAMP_PREFIX="camp_"
