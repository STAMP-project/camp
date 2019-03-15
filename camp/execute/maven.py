#
# CAMP
#
# Copyright (C) 2017 - 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from camp.execute.commons import Executor, TestResults



class MavenExecutor(Executor):


    def __init__(self, shell):
        super(MavenExecutor, self).__init__(shell)


    def _run_tests(self, path, command):
        print "   3. Running tests ..."
        self._shell.execute(self._RUN_TESTS + command, path)

    _RUN_TESTS = "docker-compose exec -it tests mvn test "


    def _collect_results(self, path):
        return TestResults(path, 3, 3, 4)
