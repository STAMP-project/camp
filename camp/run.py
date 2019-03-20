#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.yaml import YAML
from camp.core import Camp
from camp.commands import Command
from camp.generate import Z3Problem
from camp.realize import Builder

from sys import argv



def main():
    camp = Camp(YAML(), Z3Problem, Builder())
    command = Command.extract_from(argv[1:])
    command.send_to(camp)
