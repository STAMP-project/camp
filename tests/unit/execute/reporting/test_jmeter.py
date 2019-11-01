#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.report import FailedTest, SuccessfulTest, \
    TestSuite, ErroneousTest
from camp.execute.reporting.jmeter import JMeterJSONReader, \
    JMeterJSONInvalidReport

from unittest import TestCase

import json


class TheJMeterJSONReaderShould(TestCase):

    def setUp(self):
        self._reader = JMeterJSONReader()


    def test_raise_exception_when_given_empty_JSON_report(self):
        json_report = """{}"""

        with self.assertRaises(JMeterJSONInvalidReport):
            self._reader._extract_from_text(json_report)

    def test_raise_exception_when_given_empty_JSON_report_from_file(self):

        with open('tests/unit/execute/reporting/data_folder/empty_jmeter_report.json') as json_report:
            with self.assertRaises(JMeterJSONInvalidReport):
                self._reader._extract_from_text(json_report.read())

    def test_extract_a_successful_test_from_JSON(self):
        jmeter_sample_report = """{
     "transaction" : "Home page-0",
     "sampleCount" : 6,
     "errorCount" : 0,
     "errorPct" : 0.0,
     "meanResTime" : 312.16666666666674,
     "minResTime" : 4.0,
     "maxResTime" : 1362.0,
     "pct1ResTime" : 1362.0,
     "pct2ResTime" : 1362.0,
     "pct3ResTime" : 1362.0,
     "throughput" : 0.054574230048571065,
     "receivedKBytesPerSec" : 0.010232668134107075,
     "sentKBytesPerSec" : 0.020483101317058085
   }"""

        test = self._reader._extract_test_from(json.loads(jmeter_sample_report))

        self.assertIsInstance(test, SuccessfulTest)
        self.assertEqual("Home page-0", test.identifier)

    def test_extract_a_failed_test_from_JSON(self):
        jmeter_sample_report = """{
     "transaction" : "Home page-0",
     "sampleCount" : 6,
     "errorCount" : 0,
     "errorPct" : 34.5,
     "meanResTime" : 312.16666666666674,
     "minResTime" : 4.0,
     "maxResTime" : 1362.0,
     "pct1ResTime" : 1362.0,
     "pct2ResTime" : 1362.0,
     "pct3ResTime" : 1362.0,
     "throughput" : 0.054574230048571065,
     "receivedKBytesPerSec" : 0.010232668134107075,
     "sentKBytesPerSec" : 0.020483101317058085
   }"""

        test = self._reader._extract_test_from(json.loads(jmeter_sample_report))

        self.assertIsInstance(test, FailedTest)
        self.assertEqual("Home page-0", test.identifier)
        self.assertEqual("34.5% of errors calling the sample", test.failure)


    def test_extract_an_erroneous_test_from_JSON(self):
        jmeter_sample_report = """{
     "transaction" : "Home page-0",
     "sampleCount" : 6,
     "errorCount" : 0,
     "errorPct" : 100,
     "meanResTime" : 312.16666666666674,
     "minResTime" : 4.0,
     "maxResTime" : 1362.0,
     "pct1ResTime" : 1362.0,
     "pct2ResTime" : 1362.0,
     "pct3ResTime" : 1362.0,
     "throughput" : 0.054574230048571065,
     "receivedKBytesPerSec" : 0.010232668134107075,
     "sentKBytesPerSec" : 0.020483101317058085
   }"""

        test = self._reader._extract_test_from(json.loads(jmeter_sample_report))

        self.assertIsInstance(test, ErroneousTest)
        self.assertEqual("Home page-0", test.identifier)
        self.assertEqual("No successful call to sample", test.error)


    def test_raise_exception_when_given_empty_JSON_report_no_label_column(self):
        json_report = """{
   "Home page-0" : {
     "sampleCount" : 6,
     "errorCount" : 0,
     "errorPct" : 0.0,
     "meanResTime" : 312.16666666666674,
     "minResTime" : 4.0,
     "maxResTime" : 1362.0,
     "pct1ResTime" : 1362.0,
     "pct2ResTime" : 1362.0,
     "pct3ResTime" : 1362.0,
     "throughput" : 0.054574230048571065,
     "receivedKBytesPerSec" : 0.010232668134107075,
     "sentKBytesPerSec" : 0.020483101317058085
   },
   "Test case creation page" : {
     "sampleCount" : 12,
     "errorCount" : 0,
     "meanResTime" : 58.91666666666668,
     "minResTime" : 9.0,
     "maxResTime" : 479.0,
     "pct1ResTime" : 346.4000000000005,
     "pct2ResTime" : 479.0,
     "pct3ResTime" : 479.0,
     "throughput" : 0.09469995896335112,
     "receivedKBytesPerSec" : 0.5705271779017645,
     "sentKBytesPerSec" : 0.04337332104864421}}"""

        with self.assertRaises(JMeterJSONInvalidReport):
            self._reader._extract_from_text(json_report)

    def test_raise_exception_when_given_invalid_JSON_report_no_error_percentage_column(self):
        json_report = """{
  "Home page-0" : {
    "transaction" : "Home page-0",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 312.16666666666674,
    "minResTime" : 4.0,
    "maxResTime" : 1362.0,
    "pct1ResTime" : 1362.0,
    "pct2ResTime" : 1362.0,
    "pct3ResTime" : 1362.0,
    "throughput" : 0.054574230048571065,
    "receivedKBytesPerSec" : 0.010232668134107075,
    "sentKBytesPerSec" : 0.020483101317058085
  },
  "Test case creation page" : {
    "transaction" : "Test case creation page",
    "sampleCount" : 12,
    "errorCount" : 0,
    "meanResTime" : 58.91666666666668,
    "minResTime" : 9.0,
    "maxResTime" : 479.0,
    "pct1ResTime" : 346.4000000000005,
    "pct2ResTime" : 479.0,
    "pct3ResTime" : 479.0,
    "throughput" : 0.09469995896335112,
    "receivedKBytesPerSec" : 0.5705271779017645,
    "sentKBytesPerSec" : 0.04337332104864421}}"""


        with self.assertRaises(JMeterJSONInvalidReport):
            self._reader._extract_from_text(json_report)

    def test_raise_exception_when_given_invalid_JSON_report(self):
        json_report = """{
  "Home page-0" : {
    "sampleCount" : 6,
    "errorCount" : 0,
    "meanResTime" : 312.16666666666674,
    "minResTime" : 4.0,
    "maxResTime" : 1362.0,
    "pct1ResTime" : 1362.0,
    "pct2ResTime" : 1362.0,
    "pct3ResTime" : 1362.0,
    "throughput" : 0.054574230048571065,
    "receivedKBytesPerSec" : 0.010232668134107075,
    "sentKBytesPerSec" : 0.020483101317058085
  },
  "Test case creation page" : {
    "sampleCount" : 12,
    "errorCount" : 0,
    "meanResTime" : 58.91666666666668,
    "minResTime" : 9.0,
    "maxResTime" : 479.0,
    "pct1ResTime" : 346.4000000000005,
    "pct2ResTime" : 479.0,
    "pct3ResTime" : 479.0,
    "throughput" : 0.09469995896335112,
    "receivedKBytesPerSec" : 0.5705271779017645,
    "sentKBytesPerSec" : 0.04337332104864421}}"""

        with self.assertRaises(JMeterJSONInvalidReport):
            self._reader._extract_from_text(json_report)

    def test_raise_exception_when_given_invalid_JSON_report_from_file(self):
        with open('tests/unit/execute/reporting/data_folder/invalid_jmeter_report.json','r') as json_report:
            with self.assertRaises(JMeterJSONInvalidReport):
                self._reader._extract_from_text(json_report.read())

    def test_extract_a_testsuite_from_JSON(self):

        json_report = """{
  "Home page-0" : {
    "transaction" : "Home page-0",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 312.16666666666674,
    "minResTime" : 4.0,
    "maxResTime" : 1362.0,
    "pct1ResTime" : 1362.0,
    "pct2ResTime" : 1362.0,
    "pct3ResTime" : 1362.0,
    "throughput" : 0.054574230048571065,
    "receivedKBytesPerSec" : 0.010232668134107075,
    "sentKBytesPerSec" : 0.020483101317058085
  },
  "Test case creation page" : {
    "transaction" : "Test case creation page",
    "sampleCount" : 12,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 58.91666666666668,
    "minResTime" : 9.0,
    "maxResTime" : 479.0,
    "pct1ResTime" : 346.4000000000005,
    "pct2ResTime" : 479.0,
    "pct3ResTime" : 479.0,
    "throughput" : 0.09469995896335112,
    "receivedKBytesPerSec" : 0.5705271779017645,
    "sentKBytesPerSec" : 0.04337332104864421
  },
  "Save new test case" : {
    "transaction" : "Save new test case",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 59.66666666666667,
    "minResTime" : 42.0,
    "maxResTime" : 128.0,
    "pct1ResTime" : 128.0,
    "pct2ResTime" : 128.0,
    "pct3ResTime" : 128.0,
    "throughput" : 0.054262794714803796,
    "receivedKBytesPerSec" : 0.2956898383873098,
    "sentKBytesPerSec" : 0.06072769799137222
  }}
"""

        test_suite = self._reader._extract_from_text(json_report)

        self.assertIsInstance(test_suite, TestSuite)
        self.assertEqual(3, test_suite.run_test_count)

    def test_extract_a_successful_testsuite_from_JSON(self):

        json_report = """{
  "Home page-0" : {
    "transaction" : "Home page-0",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 312.16666666666674,
    "minResTime" : 4.0,
    "maxResTime" : 1362.0,
    "pct1ResTime" : 1362.0,
    "pct2ResTime" : 1362.0,
    "pct3ResTime" : 1362.0,
    "throughput" : 0.054574230048571065,
    "receivedKBytesPerSec" : 0.010232668134107075,
    "sentKBytesPerSec" : 0.020483101317058085
  },
  "Test case creation page" : {
    "transaction" : "Test case creation page",
    "sampleCount" : 12,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 58.91666666666668,
    "minResTime" : 9.0,
    "maxResTime" : 479.0,
    "pct1ResTime" : 346.4000000000005,
    "pct2ResTime" : 479.0,
    "pct3ResTime" : 479.0,
    "throughput" : 0.09469995896335112,
    "receivedKBytesPerSec" : 0.5705271779017645,
    "sentKBytesPerSec" : 0.04337332104864421
  },
  "Save new test case" : {
    "transaction" : "Save new test case",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 59.66666666666667,
    "minResTime" : 42.0,
    "maxResTime" : 128.0,
    "pct1ResTime" : 128.0,
    "pct2ResTime" : 128.0,
    "pct3ResTime" : 128.0,
    "throughput" : 0.054262794714803796,
    "receivedKBytesPerSec" : 0.2956898383873098,
    "sentKBytesPerSec" : 0.06072769799137222
  },
  "Home page-1" : {
    "transaction" : "Home page-1",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 475.8333333333333,
    "minResTime" : 8.0,
    "maxResTime" : 1401.0,
    "pct1ResTime" : 1401.0,
    "pct2ResTime" : 1401.0,
    "pct3ResTime" : 1401.0,
    "throughput" : 0.05525625086337892,
    "receivedKBytesPerSec" : 0.18384574872219922,
    "sentKBytesPerSec" : 0.022753631947322377
  },
  "Show recorded execution" : {
    "transaction" : "Show recorded execution",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 11.333333333333332,
    "minResTime" : 9.0,
    "maxResTime" : 15.0,
    "pct1ResTime" : 15.0,
    "pct2ResTime" : 15.0,
    "pct3ResTime" : 15.0,
    "throughput" : 0.055062036561192275,
    "receivedKBytesPerSec" : 0.27697709992841935,
    "sentKBytesPerSec" : 0.02548770051758314
  },
  "Home page" : {
    "transaction" : "Home page",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 789.6666666666667,
    "minResTime" : 12.0,
    "maxResTime" : 2766.0,
    "pct1ResTime" : 2766.0,
    "pct2ResTime" : 2766.0,
    "pct3ResTime" : 2766.0,
    "throughput" : 0.054570259208731244,
    "receivedKBytesPerSec" : 0.19179527626193724,
    "sentKBytesPerSec" : 0.04295276261937244
  },
  "Login" : {
    "transaction" : "Login",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 76.0,
    "minResTime" : 18.0,
    "maxResTime" : 312.0,
    "pct1ResTime" : 312.0,
    "pct2ResTime" : 312.0,
    "pct3ResTime" : 312.0,
    "throughput" : 0.05586748233190871,
    "receivedKBytesPerSec" : 0.19346298080951982,
    "sentKBytesPerSec" : 0.05897729336014972
  }}
 """

        test_suite = self._reader._extract_from_text(json_report)

        self.assertIsInstance(test_suite, TestSuite)
        self.assertEqual(7, test_suite.run_test_count)
        self.assertEqual(7, test_suite.passed_test_count)
        self.assertEqual(0, test_suite.failed_test_count)
        self.assertEqual(0, test_suite.erroneous_test_count)

    def test_extract_a_testsuite_with_failed_tests_from_JSON(self):

        json_report = """{
  "Home page-0" : {
    "transaction" : "Home page-0",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 312.16666666666674,
    "minResTime" : 4.0,
    "maxResTime" : 1362.0,
    "pct1ResTime" : 1362.0,
    "pct2ResTime" : 1362.0,
    "pct3ResTime" : 1362.0,
    "throughput" : 0.054574230048571065,
    "receivedKBytesPerSec" : 0.010232668134107075,
    "sentKBytesPerSec" : 0.020483101317058085
  },
  "Test case creation page" : {
    "transaction" : "Test case creation page",
    "sampleCount" : 12,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 58.91666666666668,
    "minResTime" : 9.0,
    "maxResTime" : 479.0,
    "pct1ResTime" : 346.4000000000005,
    "pct2ResTime" : 479.0,
    "pct3ResTime" : 479.0,
    "throughput" : 0.09469995896335112,
    "receivedKBytesPerSec" : 0.5705271779017645,
    "sentKBytesPerSec" : 0.04337332104864421
  },
  "Save new test case" : {
    "transaction" : "Save new test case",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 59.66666666666667,
    "minResTime" : 42.0,
    "maxResTime" : 128.0,
    "pct1ResTime" : 128.0,
    "pct2ResTime" : 128.0,
    "pct3ResTime" : 128.0,
    "throughput" : 0.054262794714803796,
    "receivedKBytesPerSec" : 0.2956898383873098,
    "sentKBytesPerSec" : 0.06072769799137222
  },
  "Home page-1" : {
    "transaction" : "Home page-1",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 0.0,
    "meanResTime" : 475.8333333333333,
    "minResTime" : 8.0,
    "maxResTime" : 1401.0,
    "pct1ResTime" : 1401.0,
    "pct2ResTime" : 1401.0,
    "pct3ResTime" : 1401.0,
    "throughput" : 0.05525625086337892,
    "receivedKBytesPerSec" : 0.18384574872219922,
    "sentKBytesPerSec" : 0.022753631947322377
  },
  "Show recorded execution" : {
    "transaction" : "Show recorded execution",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 100,
    "meanResTime" : 11.333333333333332,
    "minResTime" : 9.0,
    "maxResTime" : 15.0,
    "pct1ResTime" : 15.0,
    "pct2ResTime" : 15.0,
    "pct3ResTime" : 15.0,
    "throughput" : 0.055062036561192275,
    "receivedKBytesPerSec" : 0.27697709992841935,
    "sentKBytesPerSec" : 0.02548770051758314
  },
  "Home page" : {
    "transaction" : "Home page",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 10.0,
    "meanResTime" : 789.6666666666667,
    "minResTime" : 12.0,
    "maxResTime" : 2766.0,
    "pct1ResTime" : 2766.0,
    "pct2ResTime" : 2766.0,
    "pct3ResTime" : 2766.0,
    "throughput" : 0.054570259208731244,
    "receivedKBytesPerSec" : 0.19179527626193724,
    "sentKBytesPerSec" : 0.04295276261937244
  },
  "Login" : {
    "transaction" : "Login",
    "sampleCount" : 6,
    "errorCount" : 0,
    "errorPct" : 2.3,
    "meanResTime" : 76.0,
    "minResTime" : 18.0,
    "maxResTime" : 312.0,
    "pct1ResTime" : 312.0,
    "pct2ResTime" : 312.0,
    "pct3ResTime" : 312.0,
    "throughput" : 0.05586748233190871,
    "receivedKBytesPerSec" : 0.19346298080951982,
    "sentKBytesPerSec" : 0.05897729336014972
  }}
 """

        test_suite = self._reader._extract_from_text(json_report)

        self.assertIsInstance(test_suite, TestSuite)
        self.assertEqual(7, test_suite.run_test_count)
        self.assertEqual(4, test_suite.passed_test_count)
        self.assertEqual(2, test_suite.failed_test_count)
        self.assertEqual(1, test_suite.erroneous_test_count)


    def test_extract_a_testsuite_from_actual_JSON_report_on_file(self):

        with open('tests/unit/execute/reporting/data_folder/statistics.json', 'r') as json_report:

            test_suite = self._reader._extract_from_text(json_report.read())

            self.assertIsInstance(test_suite, TestSuite)
            self.assertEqual(22, test_suite.run_test_count)
            self.assertEqual(22, test_suite.passed_test_count)
            self.assertEqual(0, test_suite.failed_test_count)
            self.assertEqual(0, test_suite.erroneous_test_count)
