#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.commons import SimulatedShell
from camp.execute.select import select_executor, TechnologyNotSupported
from camp.execute.maven import MavenExecutor

from unittest import TestCase



class ExecutorFactoryShould(TestCase):


    def setUp(self):
        self._shell = SimulatedShell(None, None)


    def test_build_a_maven_executor(self):
        executor = select_executor("maven", self._shell)
        self.assertIsInstance(executor, MavenExecutor)


    def test_raise_an_exception_when_technology_is_not_supported(self):
        with self.assertRaises(TechnologyNotSupported):
            executor = select_executor("unknown_techno", self._shell)
