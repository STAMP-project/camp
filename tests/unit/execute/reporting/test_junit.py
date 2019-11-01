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
from camp.execute.reporting.junit import JUnitXMLReader, \
    JUnitXMLElementNotSupported

from unittest import TestCase



class TheJUnitXMLReaderShould(TestCase):

    def setUp(self):
        self._reader = JUnitXMLReader()


    def test_raise_exception_when_given_invalid_XML(self):
        xml = "<invalid-element name=\"foo\"/>"

        with self.assertRaises(JUnitXMLElementNotSupported):
            self._reader._extract_from_text(xml)


    def test_extract_a_successful_test_from_XML(self):
        xml = "<testcase name=\"foo\"></testcase>"

        test = self._reader._extract_from_text(xml)

        self.assertIsInstance(test, SuccessfulTest)
        self.assertEquals("foo", test.identifier)


    def test_extract_a_failed_test_from_XML(self):
        xml = ("<testcase name=\"foo\">"
               "  <failure message=\"Something happened!\"/>"
               "</testcase>")

        test = self._reader._extract_from_text(xml)

        self.assertIsInstance(test, FailedTest)
        self.assertEquals("foo", test.identifier)
        self.assertEquals("Something happened!", test.failure)


    def test_extract_an_erroneous_test(self):
        xml = ("<testcase name=\"foo\">"
               "  <error message=\"An error occurred!\"/>"
               "</testcase>")

        test = self._reader._extract_from_text(xml)

        self.assertIsInstance(test, ErroneousTest)
        self.assertEquals("foo", test.identifier)
        self.assertEquals("An error occurred!", test.error)


    def test_extract_a_test_suite(self):
        xml = (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
            "<testsuite name=\"org.samples.mysuite\">"
            "  <testcase name=\"Test 1\"/>"
            "  <testcase name=\"Test 2\"/>"
            "  <testcase name=\"Test 3\">"
            "    <failure message=\"Something happened!\"/>"
            "  </testcase>"
            "</testsuite>"
        )

        test = self._reader._extract_from_text(xml)

        self.assertIsInstance(test, TestSuite)
        self.assertEquals("org.samples.mysuite", test.identifier)
        self.assertEquals(3, test.run_test_count)
        self.assertEquals(2, test.passed_test_count)
        self.assertEquals(1, test.failed_test_count)
        self.assertEquals(0, test.erroneous_test_count)
