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
from camp.execute.commons import SimulatedShell
from camp.execute.maven import MavenExecutor, JUnitXMLReader, \
    JUnitXMLElementNotSupported

from mock import MagicMock

from os import getcwd, getuid
from os.path import join as join_paths

from StringIO import StringIO

from unittest import TestCase



class TheMavenExecutorShould(TestCase):


    def setUp(self):
        self._log = StringIO()
        self._shell = SimulatedShell(self._log, "./")
        self._execute = MavenExecutor(self._shell)
        self._configurations = [
            ("./out/config_1", None),
            ("./out/config_2", None)
        ]
        self._component = "FooBar"


    def test_build_all_images_for_all_configurations(self):
        self._call_execute()

        for each_path, _ in self._configurations:
            path = join_paths(each_path, "images")
            expected_command = MavenExecutor._BUILD_IMAGES
            self._verify(path, expected_command)


    def test_start_services_for_all_configurations(self):
        self._call_execute()

        for each_path, _ in self._configurations:
            expected_command = MavenExecutor._START_SERVICES
            self._verify(each_path, expected_command)


    def test_run_tests_for_all_configurations(self):
        self._call_execute()

        for each_path, _ in self._configurations:
            expected_command = MavenExecutor.RUN_TESTS.format(
                uid=getuid(),
                path=join_paths(getcwd(), each_path),
                component=self._component,
                settings="")
            expected = SimulatedShell.LOG_OUTPUT.format(each_path,
                                                        expected_command)
            self._verify(each_path, expected_command)


    def test_run_tests_accounting_for_settings_xml_when_it_exists(self):
        self._execute._has_XML_settings = MagicMock(returnvalue=True)

        self._call_execute()

        for each_path, _ in self._configurations:
            expected_command = MavenExecutor.RUN_TESTS.format(
                uid=getuid(),
                path=join_paths(getcwd(), each_path),
                component=self._component,
                settings="-gs settings.xml")
            self._verify(each_path, expected_command)


    def test_fetch_test_reports(self):
        self._call_execute()

        for each_path, _ in self._configurations:
            docker_ps = MavenExecutor.GET_CONTAINER_ID.format(
                configuration=each_path[6:],
                component=self._component)
            self._verify(each_path, docker_ps)

            docker_cp = MavenExecutor.FETCH_TEST_REPORTS.format(
                container="",
                component=self._component)
            self._verify(each_path, docker_cp)


    def test_stop_services_for_all_configurations(self):
        self._call_execute()

        for each_path, _ in self._configurations:
            expected_command = MavenExecutor._STOP_SERVICES
            self._verify(each_path, expected_command)


    def _call_execute(self):
        self._execute(self._configurations, self._component)


    def _verify(self, path, command):
        expected = SimulatedShell.LOG_OUTPUT.format(path,command)
        self.assertIn(expected, self._log.getvalue())



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
