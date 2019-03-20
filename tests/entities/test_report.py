#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.report import FailedTest, ErroneousTest, \
    SuccessfulTest, TestSuite, TestReport

from unittest import TestCase



class ATestShould(object):

    def setUp(self):
        self._identifier = "Foo Test"

    def test_have_no_child(self):
        self.assertEquals([], self._testcase.children)

    def test_have_run_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.run_test_count)

    def test_expose_their_identifier(self):
        self.assertEquals(self._identifier, self._testcase.identifier)



class ASuccessfulTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._testcase = SuccessfulTest(self._identifier)

    def test_have_failed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.erroneous_test_count)

    def test_have_passed_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.passed_test_count)



class AFailedTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._testcase = FailedTest(self._identifier,
                                    "There was an error")

    def test_have_passed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.passed_test_count)

    def test_have_failed_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.erroneous_test_count)

    def test_expose_its_failure(self):
        self.assertEquals("There was an error",
                          self._testcase.failure)



class AnErroneousTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._testcase = ErroneousTest(self._identifier,
                                       "There was an error")

    def test_have_passed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.passed_test_count)

    def test_have_failed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.erroneous_test_count)

    def test_expose_its_error(self):
        self.assertEquals("There was an error",
                          self._testcase.error)


class ATestSuiteShould(TestCase):

    def setUp(self):
        self._suite = TestSuite("My test suite",
            SuccessfulTest("Test 1"),
            SuccessfulTest("Test 2"),
            FailedTest("Test 3", "failure"),
            ErroneousTest("Test 4", "error"),
            TestSuite("My inner test suite",
                SuccessfulTest("Test 5"),
                SuccessfulTest("Test 6"),
                FailedTest("Test 7", "failure")
        ))

    def test_account_for_all_tests_run(self):
        self.assertEquals(7, self._suite.run_test_count)


    def test_account_for_all_tests_passed(self):
        self.assertEquals(4, self._suite.passed_test_count)


    def test_account_for_all_tests_failed(self):
        self.assertEquals(2, self._suite.failed_test_count)


    def test_account_for_all_erroneous_tests(self):
        self.assertEquals(1, self._suite.erroneous_test_count)



class ATestReportShould(TestCase):


    def setUp(self):
        self._tests = TestSuite("Fake Test Suite",
                                SuccessfulTest("Test 1"),
                                SuccessfulTest("Test 2"),
                                SuccessfulTest("Test 3"),
                                FailedTest("Test 4", "Assertion failed!"),
                                ErroneousTest("Test 5", "Unknown Error"))
        self._report = TestReport("./config", self._tests)


    def test_expose_the_number_of_passed_tests(self):
        self.assertEquals(self._tests.passed_test_count,
                          self._report.passed_test_count)


    def test_expose_the_number_of_failed_tests(self):
        self.assertEquals(self._tests.failed_test_count,
                          self._report.failed_test_count)


    def test_expose_the_number_of_erroneous_tests(self):
        self.assertEquals(self._tests.erroneous_test_count,
                          self._report.error_test_count)

    def test_expose_the_number_of_run_tests(self):
        self.assertEquals(self._tests.run_test_count,
                          self._report.run_test_count)

    def test_expose_the_path_to_related_configuration(self):
        self.assertEquals("./config",
                          self._report.configuration_name)
