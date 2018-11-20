#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp import About
from camp.codecs.yaml import YAML
from camp.core import Camp
from camp.commands import Command
from camp.generate import Z3Problem
from camp.realize import Builder

from sys import argv



class Runner(object):


    def __init__(self, camp):
        self._camp = camp


    def start(self, command_line):
        command = Command.extract_from(command_line)
        self._welcome()
        command.send_to(self._camp)
        self._goodbye()


    @staticmethod
    def _welcome():
        print "%s v%s (%s)" % (About.PROGRAM, About.VERSION, About.LICENSE)
        print About.COPYRIGHT
        print


    @staticmethod
    def _goodbye():
        print
        print "That's all folks!"



def main():
    runner = Runner(Camp(
        YAML(),
        Z3Problem,
        Builder()
    ))

    runner.start(argv[1:])
