#
# CAMP
#
# Copyright (C) 2017 - 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.commons import SimulatedShell, FailedTest, SuccessfulTest, \
    TestSuite, ErroneousTest
from camp.execute.maven import MavenExecutor, JUnitXMLReader, \
    JUnitXMLElementNotSupported

from StringIO import StringIO

from unittest import TestCase



class TheMavenExecutorShould(TestCase):


    def setUp(self):
        self._log = StringIO()
        self._shell = SimulatedShell(self._log, "./")
        self._execute = MavenExecutor(self._shell)


    def test_build_deploy_run_and_collect_test_results(self):
        configurations = [("out/config_1", None),
                          ("out/config_2", None)]
        self._execute(configurations, "whatever")

        self.assertIn("bash build_images.sh", self._log.getvalue())
        self.assertIn("docker-compose up -d", self._log.getvalue())
        self.assertIn("docker-compose exec -it tests mvn test", self._log.getvalue())



class TheJUnitXMLReaderShould(TestCase):

    def setUp(self):
        self._reader = JUnitXMLReader()


    def test_raise_exception_when_given_invalid_XML(self):
        xml = "<invalid-element name=\"foo\"/>"

        with self.assertRaises(JUnitXMLElementNotSupported):
            test = self._reader._extract_from_text(xml)


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
