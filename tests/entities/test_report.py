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
    SuccessfulTest, TestSuite, TestReport, Verdict

from deepdiff import DeepDiff

from pprint import pprint

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

    def test_export_itself_as_a_dictionary(self):
        expected = {
            "identifier": self._testcase.identifier,
            "verdict": Verdict.PASS
        }
        self.assertEquals(expected,
                          self._testcase.as_dictionary)



class AFailedTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._failure = "There was a failure!"
        self._testcase = FailedTest(self._identifier,
                                    self._failure)

    def test_have_passed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.passed_test_count)

    def test_have_failed_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.erroneous_test_count)

    def test_expose_its_failure(self):
        self.assertEquals(self._failure,
                          self._testcase.failure)

    def test_export_itself_as_a_dictionary(self):
        expected = {
            "identifier": self._testcase.identifier,
            "verdict": Verdict.FAIL,
            "failure": self._failure
        }
        self.assertEquals(expected,
                          self._testcase.as_dictionary)



class AnErroneousTestShould(TestCase, ATestShould):

    def setUp(self):
        ATestShould.setUp(self)
        self._error = "There was an error!"
        self._testcase = ErroneousTest(self._identifier,
                                       self._error)

    def test_have_passed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.passed_test_count)

    def test_have_failed_test_count_equals_to_zero(self):
        self.assertEquals(0, self._testcase.failed_test_count)

    def test_have_erroneous_test_count_equals_to_one(self):
        self.assertEquals(1, self._testcase.erroneous_test_count)

    def test_expose_its_error(self):
        self.assertEquals(self._error,
                          self._testcase.error)


    def test_export_itself_as_a_dictionary(self):
        expected = {
            "identifier": self._testcase.identifier,
            "verdict": Verdict.ERROR,
            "error": self._error
        }
        self.assertEquals(expected,
                          self._testcase.as_dictionary)


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


    def test_export_itself_as_a_dictionary(self):
        expected = {
            "identifier": "My test suite",
            "tests": [
                {
                    "identifier": "Test 1" ,
                    "verdict": Verdict.PASS
                },
                {
                    "identifier": "Test 2" ,
                    "verdict": Verdict.PASS
                },
                {
                    "identifier": "Test 3" ,
                    "verdict": Verdict.FAIL,
                    "failure": "failure"
                },
                {
                    "identifier": "Test 4" ,
                    "verdict": Verdict.ERROR,
                    "error": "error"
                },
                {
                    "identifier": "My inner test suite",
                    "tests": [
                        {
                            "identifier": "Test 5" ,
                            "verdict": Verdict.PASS
                        },
                        {
                            "identifier": "Test 6" ,
                            "verdict": Verdict.PASS
                        },
                        {
                            "identifier": "Test 7" ,
                            "verdict": Verdict.FAIL,
                            "failure": "failure"
                        }
                    ]
                }
            ]
        }
        actual = self._suite.as_dictionary
        differences = DeepDiff(expected, actual, ignore_order=True)
        self.assertEquals(len(differences), 0,
                          str(actual))



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


    def test_export_itself_as_a_dictionary(self):
        expected = {
            "path": "./config",
            "tests": {
                "identifier": "Fake Test Suite",
                "tests": [
                    {
                        "identifier": "Test 1",
                        "verdict": Verdict.PASS
                    },
                    {
                        "identifier": "Test 2",
                        "verdict": Verdict.PASS
                    },
                    {
                        "identifier": "Test 3",
                        "verdict": Verdict.PASS
                    },
                    {
                        "identifier": "Test 4",
                        "verdict": Verdict.FAIL,
                        "failure": "Assertion failed!"
                    },
                    {
                        "identifier": "Test 5",
                        "verdict": Verdict.ERROR,
                        "error": "Unknown Error"
                    }
                ]
            }
        }
        actual = self._report.as_dictionary
        differences = DeepDiff(expected, actual, ignore_order=True)
        self.assertEquals(len(differences), 0, pprint(differences))
