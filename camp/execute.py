#
# CAMP
#
# Copyright (C) 2017 - 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



class TestResults:

    def __init__(self, name, passed, failed, error):
        self._name = name
        self._passed = passed
        self._failed = failed
        self._error = error

    @property
    def configuration_name(self):
        return self._name


    @property
    def failed_test_count(self):
        return self._failed

    @property
    def passed_test_count(self):
        return self._passed

    @property
    def error_test_count(self):
        return self._error

    @property
    def run_test_count(self):
        return self.passed_test_count + \
            self.failed_test_count + \
            self.error_test_count



class Executor:


    def __call__(self, configurations):
        return [ TestResults(each, 2, 3, 4) for each, _ in configurations ]
