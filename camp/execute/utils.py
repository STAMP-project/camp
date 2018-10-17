#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

import sys


def output_message(message):
	sys.stdout.write(message)

def output_message_error(message):
	sys.stderr.write(message)


class FileNotFoundError(Exception):

        def __init__(self, missing_file):
                self._missing_file = missing_file

        def __str__(self):
                return "Could not access file '%s'" % self._missing_file

        
