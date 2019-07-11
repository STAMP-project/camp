#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

import json

from camp.entities.report import SuccessfulTest, FailedTest, \
	ErroneousTest, TestSuite
from camp.execute.reporting.commons import ReportReader


class JMeterJSONReader(ReportReader):
	"""
	Extracts camp.execute.TestSuite objects from JMeter JSON Agregate report
	"""

	TRANSACTION = "transaction"
	NUM_OF_SAMPLES = "sampleCount"
	ERR_COUNT = "errorCount"
	ERR_PERCENTAGE = "errorPct"
	AVG_RESP_TIME = "meanResTime"
	MIN_RESP_TIME = "minResTime"
	MAX_RESP_TIME = "maxResTime"
	PERCENTILE_RESP_TIME_1 = "pct1ResTime"
	PERCENTILE_RESP_TIME_2 = "pct2ResTime"
	PERCENTILE_RESP_TIME_3 = "pct3ResTime"
	THROUGHPUT = "throughput"
	RECEIVED_BYTES_PER_SEC = "receivedKBytesPerSec"
	SENT_BYTES_PER_SEC = "sentKBytesPerSec"


	def _extract_from_text(self, json_report):

    	# TODO: currently it doesn't take into account all JMeter report fields

		tests = []

		json_report = json.load(json_report)

		if not json_report:
			raise JMeterJSONInvalidReport("Empty JMeter Report: " + json.dumps(json_report))

		for sample,sample_data in json_report.items():
			test = self._extract_test_from(sample_data)
			tests.append(test)
        
		return TestSuite("all samples", *tests)



	def _extract_test_from(self, jmeter_sample_data):
		if self.TRANSACTION not in jmeter_sample_data:
			raise JMeterJSONInvalidReport("No URL Label present in JMeter Report: "  + json.dumps(jmeter_sample_data))
		if self.ERR_PERCENTAGE not in jmeter_sample_data:
			raise JMeterJSONInvalidReport("No error percentage value present in JMeter Report: "  + json.dumps(jmeter_sample_data))

		identifier = jmeter_sample_data[self.TRANSACTION]
		error_percentage = jmeter_sample_data[self.ERR_PERCENTAGE]
		if float(error_percentage) == 100:
			message = "No successful call to sample"
			return ErroneousTest(identifier, message)

		if float(error_percentage) > 0:
			message = str(error_percentage) + "% of errors calling the sample"
			return FailedTest(identifier, message)

		return SuccessfulTest(identifier)

class JMeterJSONInvalidReport(Exception):


	def __init__(self, element):
		self._element = element


	def __str__(self):
		return self._element
