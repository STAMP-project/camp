#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



class TestReport:

    def __init__(self, name, test=None):
        self._name = name
        self._test = test


    @property
    def configuration_name(self):
        return self._name

    @property
    def failed_test_count(self):
        if not self._test:
            return 0
        return self._test.failed_test_count

    @property
    def passed_test_count(self):
        if not self._test:
            return 0
        return self._test.passed_test_count

    @property
    def error_test_count(self):
        if not self._test:
            return 0
        return self._test.erroneous_test_count

    @property
    def run_test_count(self):
        if not self._test:
            return 0
        return self._test.run_test_count



class Verdict:
    PASS = 1
    FAIL = 2
    ERROR = 3



class Test(object):

    def __init__(self, identifier, verdict):
        self._identifier = identifier
        self._verdict = verdict


    @property
    def identifier(self):
        return self._identifier


    @property
    def children(self):
        return []


    @property
    def run_test_count(self):
        return 1


    @property
    def passed_test_count(self):
        return 1 if self._verdict == Verdict.PASS \
            else 0


    @property
    def failed_test_count(self):
        return 1 if self._verdict == Verdict.FAIL \
            else 0


    @property
    def erroneous_test_count(self):
        return 1 if self._verdict == Verdict.ERROR \
            else 0


class SuccessfulTest(Test):

    def __init__(self, identifier):
        super(SuccessfulTest, self).__init__(identifier, Verdict.PASS)



class FailedTest(Test):

    def __init__(self, identifier, failure):
        super(FailedTest, self).__init__(identifier, Verdict.FAIL)
        self._failure = failure


    @property
    def failure(self):
        return self._failure



class ErroneousTest(Test):

    def __init__(self, identifier, error):
        super(ErroneousTest, self).__init__(identifier, Verdict.ERROR)
        self._error = error


    @property
    def error(self):
        return self._error



class TestSuite(Test):

    def __init__(self, identifier, *tests):
        super(TestSuite, self).__init__(identifier, None)
        self._tests = tests

    @Test.run_test_count.getter
    def run_test_count(self):
        return sum(each.run_test_count for each in self._tests)

    @Test.passed_test_count.getter
    def passed_test_count(self):
        return sum(each.passed_test_count for each in self._tests)

    @Test.failed_test_count.getter
    def failed_test_count(self):
        return sum(each.failed_test_count for each in self._tests)

    @Test.erroneous_test_count.getter
    def erroneous_test_count(self):
        return sum(each.erroneous_test_count for each in self._tests)
