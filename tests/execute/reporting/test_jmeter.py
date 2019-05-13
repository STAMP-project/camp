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

import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TheJMeterCSVReaderShould(TestCase):

	

    def setUp(self):
        self._reader = JMeterCSVReader()


    def test_raise_exception_when_given_empty_CSV_report(self):
        csv_report = (
        	"Label,# Samples,Average,Median,90\% Line,95\% Line,99\% Line,Min,Max,Error \%,Throughput,Received KB/sec,Sent KB/sec"
        	)


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report.splitlines())

    def test_raise_exception_when_given_empty_CSV_report_from_file(self):
    	
        csv_report = os.path.join(THIS_DIR, os.pardir, 'data_folder/empty_jmeter_report.csv')


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report)

    def test_raise_exception_when_given_empty_CSV_report_no_label_column(self):
        csv_report = (
        	"# Samples,Average,Median,90\% Line,95\% Line,99\% Line,Min,Max,Error \%,Throughput,Received KB/sec,Sent KB/sec"
        	)


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report.splitlines())

    def test_raise_exception_when_given_invalid_CSV_report_no_error_percentage_column(self):
        csv_report = (
        	"Label,# Samples,Average,Median,90\% Line,95\% Line,99\% Line,Min,Max,Throughput,Received KB/sec,Sent KB/sec"
        	)


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report.splitlines())

    def test_raise_exception_when_given_invalid_CSV_report(self):
        csv_report = (
        	"# Samples,Average,Median,90\% Line,95\% Line,99\% Line,Min,Max,Throughput,Received KB/sec,Sent KB/sec"
        	)


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report.splitlines())

    def test_raise_exception_when_given_invalid_CSV_report_from_file(self):
        csv_report = os.path.join(THIS_DIR, os.pardir, 'data_folder/invalid_jmeter_report.csv')


        with self.assertRaises(JMeterCSVInvalidReport):
            self._reader._extract_from_text(csv_report)
