#
# CAMP
#
# Copyright (C) 2017 - 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from camp.execute.commons import Executor, SuccessfulTest, FailedTest, ErroneousTest, \
    TestSuite, TestResults

from xml.etree.ElementTree import fromstring




class MavenExecutor(Executor):


    def __init__(self, shell):
        super(MavenExecutor, self).__init__(shell)


    def _run_tests(self, path, command):
        print "   3. Running tests ..."
        self._shell.execute(self._RUN_TESTS + command, path)

    _RUN_TESTS = "docker-compose exec -it tests mvn test "


    def _collect_results(self, path):
        return TestResults(path, 3, 3, 4)





class JUnitXMLReader:
    """Name of the XML elements and attributes in the JUnitXML"""

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
