#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from __future__ import unicode_literals
from __future__ import print_function

from camp.entities.report import SuccessfulTest, FailedTest, \
    ErroneousTest, TestSuite, TestReport
from camp.execute.reporting.commons import ReportReader

from os.path import abspath, join as join_paths

from xml.etree.ElementTree import fromstring



class JUnitXMLReader(ReportReader):
    """
    Extracts camp.execute.TestSuite objects from JUnit XML
    """

    ERROR = "error"
    FAILURE = "failure"
    MESSAGE = "message"
    NAME = "name"
    TEST_CASE = "testcase"
    TEST_SUITE = "testsuite"
    TEST_SUITES = "testsuites"


    def _extract_from_text(self, xml):
        root = fromstring(xml)
        if root.tag == self.TEST_SUITES:
            return self._extract_multiple_test_suites_from(root)

        if root.tag == self.TEST_SUITE:
            return self._extract_test_suite_from(root)

        if root.tag == self.TEST_CASE:
            return self._extract_test_from(root)

        raise JUnitXMLElementNotSupported(root.tag)


    def _extract_multiple_test_suites_from(self, element):
        suites = []
        for each_xml_suite in element.findall(self.TEST_SUITE):
            suite = self._extract_test_suite_from(each_xml_suite)
            suites.append(suite)
        return TestSuite("all", *suites)


    def _extract_test_suite_from(self, element):
        tests = []
        identifier = element.get(self.NAME)
        for each in element.findall(self.TEST_CASE):
            test = self._extract_test_from(each)
            tests.append(test)
        return TestSuite(identifier, *tests)


    def _extract_test_from(self, element):
        identifier = element.get(self.NAME)

        failure = element.find(self.FAILURE)
        if failure is not None:
            message = failure.get(self.MESSAGE)
            return FailedTest(identifier, message)

        error = element.find(self.ERROR)
        if error is not None:
            message = error.get(self.MESSAGE)
            return ErroneousTest(identifier, message)

        return SuccessfulTest(identifier)



class JUnitXMLElementNotSupported(Exception):

    def __init__(self, element):
        self._element = element


    def __str__(self):
        return self.RENDER.format(self._element)


    RENDER = "XML element '{}' is not yet supported!"
