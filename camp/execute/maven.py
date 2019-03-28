#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.report import SuccessfulTest, FailedTest, \
    ErroneousTest, TestSuite, TestReport
from camp.execute.commons import Executor

from os import getuid
from os.path import abspath, exists, join as join_paths

from xml.etree.ElementTree import fromstring



class MavenExecutor(Executor):


    def __init__(self, shell, xml_reader=None):
        super(MavenExecutor, self).__init__(shell)
        self._xml_reader = xml_reader or JUnitXMLReader()


    def _run_tests(self, path, component):
        print "   3. Running tests ..."
        absolute_path = abspath(path)

        settings = ""
        if self._has_XML_settings(path, component):
            settings = "-gs settings.xml"

        command = self.RUN_TESTS.format(
            uid=getuid(),
            path=absolute_path,
            component=component,
            settings=settings)
        self._shell.execute(command, path)

    RUN_TESTS = ("docker-compose run "
                 "--user={uid} "
                 "-v {path}/images/{component}_0/:/{component} "
                 "{component} "
                 "mvn test -B {settings}")


    def _has_XML_settings(self, path, component):
        directory = join_paths(path,
                               "images", component+"_0")
        results = self._shell.find_all_files("settings.xml", directory)
        return len(results) > 0


    def _collect_results(self, path):
        print "   4. Collecting tests ..."
        all_tests = []

        directory = join_paths(path,
                               "images", "tests_0", "target", "surefire-reports")
        test_reports = self._shell.find_all_files(".xml", directory)

        for each_report in test_reports:
            try:
                print "      Reading", each_report
                with open(each_report, "r") as report:
                    file_content = report.read()
                    test_suite = self._xml_reader._extract_from_text(file_content)
                    all_tests.append(test_suite)

            except JUnitXMLElementNotSupported as error:
                print "      - Error: ", str(error)

        return TestReport(path, TestSuite("all tests", *all_tests))





class JUnitXMLReader:
    """
    Extracts camp.execute.TestSuite objects from JUnit XML
    """

    ERROR = "error"
    FAILURE = "failure"
    MESSAGE = "message"
    NAME = "name"
    TEST_CASE = "testcase"
    TEST_SUITE = "testsuite"


    def _extract_from_text(self, xml):
        root = fromstring(xml)
        if root.tag == "testsuite":
            return self._extract_test_suite_from(root)

        if root.tag == "testcase":
            return self._extract_test_from(root)

        raise JUnitXMLElementNotSupported(root.tag)


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
