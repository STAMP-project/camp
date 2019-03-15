#
# CAMP
#
# Copyright (C) 2017 - 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.commons import SimulatedShell
from camp.execute.maven import MavenExecutor

from StringIO import StringIO

from unittest import TestCase



class TheMavenExecutorShould(TestCase):


    def setUp(self):
        self._log = StringIO()
        self._shell = SimulatedShell(self._log, "./")
        self._execute = MavenExecutor(self._shell)


    def test_build_deploy_run_and_collect_test_results(self):
        configurations = [("out/config_1", None),
                          ("out/config_2", None)]
        self._execute(configurations, "whatever")

        self.assertIn("bash build_images.sh", self._log.getvalue())
        self.assertIn("docker-compose up -d", self._log.getvalue())
        self.assertIn("docker-compose exec -it tests mvn test", self._log.getvalue())
