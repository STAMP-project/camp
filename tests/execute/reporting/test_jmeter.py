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
from camp.execute.reporting.jmeter import JMeterCSVReader, \
    JMeterCSVInvalidReport

from unittest import TestCase

import io

class TheJMeterCSVReaderShould(TestCase):

	

    def setUp(self):
        self._reader = JMeterCSVReader()


    def test_raise_exception_when_given_empty_CSV_report(self):
        csv_report = """Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec"""

        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(io.StringIO(csv_report))

	    

    def test_raise_exception_when_given_empty_CSV_report_from_file(self):
    	
        csv_report = open('tests/execute/reporting/data_folder/empty_jmeter_report.csv', 'r')


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report)

    def test_raise_exception_when_given_empty_CSV_report_no_label_column(self):
        csv_report = """# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec"""

        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(io.StringIO(csv_report))

    def test_raise_exception_when_given_invalid_CSV_report_no_error_percentage_column(self):
        csv_report = """Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Throughput,Received KB/sec,Sent KB/sec"""

        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(io.StringIO(csv_report))

    def test_raise_exception_when_given_invalid_CSV_report(self):
        csv_report = """# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Throughput,Received KB/sec,Sent KB/sec"""

        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(io.StringIO(csv_report))

    def test_raise_exception_when_given_invalid_CSV_report_from_file(self):
        csv_report = open('tests/execute/reporting/data_folder/invalid_jmeter_report.csv','r')


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report)

    def test_extract_a_testsuite_from_CSV(self):

        csv_report = """Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec
Open home page,13,4.9,4.5,4.6,4.7,5.0,2.1,5.1,0.0,37.16,2.58,6735.0
Login,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8
Access personal area,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,20.0,40.03,3.01,535.8
Logout,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8"""

        test_suite = self._reader._extract_from_text(io.StringIO(csv_report))

        self.assertIsInstance(test_suite, TestSuite)
        self.assertEquals(4, test_suite.run_test_count)

    def test_extract_a_successful_testsuite_from_CSV(self):

        csv_report = """Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec
Open home page,13,4.9,4.5,4.6,4.7,5.0,2.1,5.1,0.0,37.16,2.58,6735.0
Login,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8
Access personal area,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8
Logout,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8"""

        test_suite = self._reader._extract_from_text(io.StringIO(csv_report))

        self.assertIsInstance(test_suite, TestSuite)
        self.assertEquals(4, test_suite.run_test_count)
        self.assertEquals(4, test_suite.passed_test_count)
        self.assertEquals(0, test_suite.failed_test_count)
        self.assertEquals(0, test_suite.erroneous_test_count)

    def test_extract_a_testsuite_with_failed_tests_from_CSV(self):

        csv_report = """Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec
Open home page,13,4.9,4.5,4.6,4.7,5.0,2.1,5.1,0.0,37.16,2.58,6735.0
Login,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8
Access personal area,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,27.4,40.03,3.01,535.8
View roder history,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,100,40.03,3.01,535.8
Logout,13,5.1,4.3,4.2,4.9,5.3,3.7,6.1,0.0,40.03,3.01,535.8"""

        test_suite = self._reader._extract_from_text(io.StringIO(csv_report))

        self.assertIsInstance(test_suite, TestSuite)
        self.assertEquals(5, test_suite.run_test_count)
        self.assertEquals(3, test_suite.passed_test_count)
        self.assertEquals(1, test_suite.failed_test_count)
        self.assertEquals(1, test_suite.erroneous_test_count)

