#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

import csv

from camp.entities.report import SuccessfulTest, FailedTest, \
    ErroneousTest, TestSuite
from camp.execute.reporting.commons import ReportReader


class JMeterCSVReader(ReportReader):
    """
    Extracts camp.execute.TestSuite objects from JMeter CSV Agregate report
    """

    URL_LABEL = "Label"
    NUM_OF_SAMPLES = "# Samples"
    AVG_RESP_TIME = "Average"
    MEDIAN_RESP_TIME = "Median"
    PERCENTILE_RESP_TIME_90 = "90\% Line"
    PERCENTILE_RESP_TIME_95 = "95\% Line"
    PERCENTILE_RESP_TIME_99 = "99\% Line"
    MIN_RESP_TIME = "Min"
    MAX_RESP_TIME = "Max"
    ERR_PERCENTAGE = "Error \%"
    THROUGHPUT = "Throughput"
    RECEIVED_BYTES = "Received KB\/sec"
    SENT_BYTES = "Sent KB\/sec"


    def _extract_from_text(self, csvfile):

    	# TODO: currently it doesn't take into account all JMeter report fields

		tests = []

		reader = csv.DictReader(csvfile)

		if reader.line_num == 0:
			raise JMeterCSVInvalidReport("Empty JMeter Report")

		if self.URL_LABEL not in reader.fieldnames:
			raise JMeterCSVInvalidReport("No URL Label present in JMeter Report")

		if self.ERR_PERCENTAGE not in reader.fieldnames:
			raise JMeterCSVInvalidReport("No error percentage value present in JMeter Report")


		for row in reader:
			test = self._extract_test_from(row)
    		tests.append(test)


    def _extract_test_from(self, element):
    	identifier = element.get(self.URL_LABEL)
    	error_percentage = element.get(self.ERR_PERCENTAGE)
    	if error_percentage == 100:
    		message = "No successful call to sample"
    		return ErroneousTest(identifier, message)

		if error_percentage > 0:
			message = error_percentage + "% of errors calling the sample"
			return FailedTest(identifier, message)

        return SuccessfulTest(identifier)

class JMeterCSVInvalidReport(Exception):


    def __init__(self, element):
        self._element = element


    def __str__(self):
        return self._element
