#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from sys import argv

from camp import About
from camp.core import Camp
from camp.commands import Command
from camp.stacks.find import Finder as SFinder
from camp.stacks.build import Builder as SBuilder
from camp.orchestrations.find import Finder as OFinder
from camp.orchestrations.build import Builder as OBuilder
from camp.realize.engine import RealizationEngine


class Runner(object):


    def __init__(self, camp):
        self._camp = camp


    def start(self, command_line):
        command = Command.extract_from(command_line)
        self._welcome()
        command.send_to(self._camp)
        self._goodbye()


    def _welcome(self):
        print "%s v%s (%s)" % (About.PROGRAM, About.VERSION, About.LICENSE)
        print About.COPYRIGHT


    def _goodbye(self):
        print "That's all folks!"



def main():
    runner = Runner(Camp(
        SFinder(),
        SBuilder(),
        OFinder(),
        OBuilder(),
        RealizationEngine()
    ))
    runner.start(argv[1:])
