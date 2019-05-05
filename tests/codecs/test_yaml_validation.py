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

from camp.codecs.yaml import YAML, InvalidYAMLModel
from camp.entities.model import DockerFile, DockerImage, Substitution, \
    TestSettings, ResourceSelection
from camp.entities.report import SuccessfulTest, FailedTest, ErroneousTest, \
    TestSuite, TestReport

from io import BytesIO

from sys import version_info

from unittest import TestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO



class IgnoredEntriesAreReported(TestCase):

    def setUp(self):
        self._codec = YAML()


    def assert_extra_in(self, text, expected):
        try :
            self._codec.load_model_from(StringIO(text))
            fail("Should have raised an exception!")
        except InvalidYAMLModel as error:
            self.assertEqual(1, len(error.warnings))
            self.assertEqual(expected,
                             error.warnings[0].path)


    def test_when_an_extra_entry_is_in_the_root(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "extra: this entry should be reported!\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="extra")


    def test_when_an_extra_entry_is_in_a_component(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      extra: this entry should be reported!\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/extra")


    def test_when_an_extra_entry_is_in_the_variables(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      variables:\n"
                             "         memory:\n"
                             "            extra: this entry should be reported!\n"
                             "            values: [ 1GB, 2GB]\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/variables/memory/extra")


    def test_when_an_extra_entry_is_in_a_substitution(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      variables:\n"
                             "         memory:\n"
                             "            values: [ 1GB, 2GB]\n"
                             "            realization: \n"
                             "              - targets: [ file1 ]\n"
                             "                pattern: mem=1GB\n"
                             "                extra: this entry should be reported\n"
                             "                replacements: [mem=1GB, mem=2GB]\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/variables/memory/realization/#1/extra")


    def test_when_an_extra_entry_is_in_a_resource_selection(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      variables:\n"
                             "         memory:\n"
                             "            values: [ 1GB, 2GB]\n"
                             "            realization: \n"
                             "              - select: \"${value}_docker-compose.yml\"\n"
                             "                extra: this entry should be reported\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/variables/memory/realization/#1/extra")



    def test_when_an_extra_entry_is_in_the_implementation(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      implementation:\n"
                             "         extra: this entry should be reported!\n"
                             "         docker:\n"
                             "            file: DockerFile\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/implementation/extra")


    def test_when_an_extra_entry_is_in_docker(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      implementation:\n"
                             "         docker:\n"
                             "            extra: this entry should be reported!\n"
                             "            file: DockerFile\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/implementation/docker/extra")


    def test_when_an_extra_entry_is_in_the_goals(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "goals:\n"
                             "   extra: this entry should be reported!\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="goals/extra")


    def test_when_an_extra_entry_is_in_the_test_settings(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      tests:\n"
                             "        command: mvn -B test -gs ./settings.xml\n"
                             "        extra: this entry should be reported!\n"
                             "        reports:\n"
                             "          format: JUnit\n"
                             "          location: target/surefire-reports\n"
                             "          pattern: TEST*.xml\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/tests/extra")


    def test_when_an_extra_entry_is_in_the_test_reports(self):
        self.assert_extra_in("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "      tests:\n"
                             "        command: mvn -B test -gs ./settings.xml\n"
                             "        reports:\n"
                             "          extra: this entry should be reported!\n"
                             "          format: JUnit\n"
                             "          location: target/surefire-reports\n"
                             "          pattern: TEST*.xml\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expected="components/server/tests/reports/extra")




class TypeMismatchAreReported(TestCase):


    def setUp(self):
        self._codec = YAML()


    def test_with_a_string_as_component(self):
        self.assert_warning(
            "components: blablabla\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expected="dict",
            found="str", path="components")


    def test_with_a_string_as_provided_services(self):
        self.assert_warning(
            "components: \n"
            "  server:\n"
            "     provides_services: blablabla\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expected="list",
            found="str",
            path="components/server/provides_services")


    def test_with_a_string_as_required_services(self):
        self.assert_warning(
            "components: \n"
            "  server:\n"
            "     requires_services: blablabla\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expected="list",
            found="str",
            path="components/server/requires_services")


    def test_with_a_string_as_provided_features(self):
        self.assert_warning(
            "components: \n"
            "  server:\n"
            "     provides_features: blablabla\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expected="list", found="str",
            path="components/server/provides_features")


    def test_with_a_string_as_required_features(self):
        self.assert_warning(
            "components: \n"
                "  server:\n"
                "     requires_features: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n",
            expected="list",
            found="str",
            path="components/server/requires_features")


    def test_with_a_string_as_variables(self):
        self.assert_warning(
            "components: \n"
                "  server:\n"
                "     requires_features: [ Awesome ]\n"
                "     variables: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n",
            expected="dict",
            found="str",
            path="components/server/variables")


    def test_with_a_string_as_implementation(self):
        self.assert_warning(
            "components: \n"
            "  server:\n"
            "     requires_features: [ Awesome ]\n"
            "     implementation: blablabla\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expected="dict",
            found="str",
            path="components/server/implementation")


    def test_with_a_string_as_goals(self):
        self.assert_warning(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Awesome ]\n"
            "goals: blablabla\n",
            expected="dict",
            found="str",
            path="goals")


    def test_with_a_string_as_running(self):
        self.assert_warning(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Awesome ]\n"
            "goals:\n"
            "  running: blablabla\n",
            expected="list",
            found="str",
            path="goals/running")


    def test_with_a_string_as_substitution_replacements(self):
        self.assert_warning(
            "components:\n"
                "   server:\n"
                "      provides_services: [ Awesome ]\n"
                "      variables:\n"
                "        memory:\n"
                "          values: [1GB, 2GB ]\n"
                "          realization:\n"
                "             - targets: [ Dockerfile ]\n"
                "               pattern: xmem=1GB\n"
                "               replacements: This should not be a string!\n"
                "goals:\n"
                "  running: [ Awesome ]\n",
            expected="list",
            found="str",
            path="components/server/variables/memory/realization/#1/replacements",
            warning_count=2)


    def test_with_a_string_as_substitution_targets(self):
        self.assert_warning(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Awesome ]\n"
            "      variables:\n"
            "        memory:\n"
            "          values: [1GB, 2GB ]\n"
            "          realization:\n"
            "             - targets: This should not be a string!\n"
            "               pattern: xmem=1GB\n"
            "               replacements: [xmem=1GB, xmem=2GB]\n"
            "goals:\n"
            "  running: [ Awesome ]\n",
            expected="list",
            found="str",
            path="components/server/variables/memory/realization/#1/targets",
            warning_count=2)

    def test_with_a_number_as_selected_resource(self):
        self.assert_warning(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Awesome ]\n"
            "      variables:\n"
            "        memory:\n"
            "          values: [1GB, 2GB ]\n"
            "          realization:\n"
            "             - select: 123\n"
            "goals:\n"
            "  running: [ Awesome ]\n",
            expected="str",
            found="int",
            path="components/server/variables/memory/realization/#1/select",
            warning_count=1)



    def assert_warning(self, text,  expected, found, path, warning_count=1):
        try:
            model = self._codec.load_model_from(StringIO(text))
            self.fail("InvalidYAMLModel should have been thrown!")

        except InvalidYAMLModel as error:
            self.assertEqual(warning_count, len(error.warnings),
                             [str(w) for w in error.warnings])
            self.assertEqual(path,
                             error.warnings[0].path)
            self.assertEqual(found,
                             error.warnings[0].found)
            self.assertEqual(expected,
                             error.warnings[0].expected)



class TypeMismatchesAreNotReportedWhenStringIsExpected(TestCase):


    def setUp(self):
        self._codec = YAML()

    def assert_no_warning_in(self, text):
        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_boolean_among_running_items(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Awesome ]\n"
            "goals:\n"
            "  running: [ Awesome, True ]\n")


    def test_with_a_number_among_provided_services(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Awesome, 1234.5 ]\n"
            "goals:\n"
            "  running: [ Awesome ]\n")


    def test_with_a_number_among_required_services(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      requires_services: [ Awesome, 1234.5 ]\n"
            "goals:\n"
            "  running: [ Awesome ]\n")


    def test_with_a_number_among_provided_features(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      provides_features: [ Awesome, 1234.5 ]\n"
            "goals:\n"
            "  running: [ Awesome ]\n")


    def test_with_a_number_among_required_features(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      requires_features: [ Awesome, 1234.5 ]\n"
            "goals:\n"
            "  running: [ Awesome ]\n")


    def test_with_a_number_among_variable_values(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      requires_services: [ Awesome ]\n"
            "      variables:\n"
            "         memory:\n"
            "           values: [ High, 1234]\n"
            "goals:\n"
            "  running: [ Awesome ]\n")


    def test_with_a_number_among_docker_file(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      requires_services: [ Awesome ]\n"
            "      implementation:\n"
            "         docker:\n"
            "           file: 1234.5\n"
            "goals:\n"
            "  running: [ Awesome ]\n")


    def test_with_a_number_among_docker_image(self):
        self.assert_no_warning_in(
            "components:\n"
            "   server:\n"
            "      requires_services: [ Awesome ]\n"
            "      implementation:\n"
            "         docker:\n"
            "           image: 1234.5\n"
            "goals:\n"
            "  running: [ Awesome ]\n")



class MissingMandatoryEntriesAreReported(TestCase):


    def setUp(self):
        self._codec = YAML()


    def _assertItemsEqual(self, expected, actual):
        # For compatibility with Python 2.7, as the method
        # assertItemsEquals has been renamed in Python 3.3 into
        # 'assertCountEqual'.
        return self.assertEqual(sorted(expected), sorted(actual))


    def test_when_omitting_substitution_targets(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      variables:\n"
            "        memory:\n"
            "          values: [1GB, 2GB, 4GB]\n"
            "          realization:\n"
            "             - pattern: xmem=1GB\n"
            "               replacements: [xmem=1, xmem=2, xmem=4]\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/variables/memory/realization/#1",
            candidates=["targets"])


    def test_when_omitting_substitution_pattern(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      variables:\n"
            "        memory:\n"
            "          values: [1GB, 2GB, 4GB]\n"
            "          realization:\n"
            "             - targets: [ Dockerfile ]\n"
            "               replacements: [xmem=1, xmem=2, xmem=4]\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/variables/memory/realization/#1",
            candidates=["pattern"])


    def test_when_omitting_substitution_replacements(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      variables:\n"
            "        memory:\n"
            "          values: [1GB, 2GB, 4GB]\n"
            "          realization:\n"
            "             - targets: [ Dockerfile ]\n"
            "               pattern: xmem=1GB\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/variables/memory/realization/#1",
            candidates=["replacements"])


    def test_when_omitting_the_docker_file(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      implementation:\n"
            "         docker: {}\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/implementation/docker",
            candidates=["file", "image"])


    def test_when_omitting_the_testing_commands(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      tests:\n"
            "        # Missing: command: mvn -B test -gs ./settings.xml\n"
            "        reports:\n"
            "          format: JUnit\n"
            "          location: target/surefire-reports\n"
            "          pattern: TEST*.xml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/tests",
            candidates=["command"])


    def test_when_omitting_test_report_format(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      tests:\n"
            "        command: mvn -B test -gs ./settings.xml\n"
            "        reports:\n"
            "          # Missing: format: JUnit\n"
            "          location: target/surefire-reports\n"
            "          pattern: TEST*.xml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/tests/reports",
            candidates=["format"])


    def test_when_omitting_test_report_location(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      tests:\n"
            "        command: mvn -B test -gs ./settings.xml\n"
            "        reports:\n"
            "          format: JUnit\n"
            "          # Missing: location: target/surefire-reports\n"
            "          pattern: TEST*.xml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/tests/reports",
            candidates=["location"])


    def test_when_omitting_test_report_pattern(self):
        self.assert_missing(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      tests:\n"
            "        command: mvn -B test -gs ./settings.xml\n"
            "        reports:\n"
            "          format: JUnit\n"
            "          location: target/surefire-reports\n"
            "          # Missing: pattern: TEST*.xml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            path="components/server/tests/reports",
            candidates=["pattern"])


    def assert_missing(self, text, path, candidates):
        try:
            self._codec.load_model_from(StringIO(text))
            self.fail("InvalidYAMLModel should have been thrown!")

        except InvalidYAMLModel as error:
            self.assertEqual(1, len(error.warnings))
            self.assertEqual(path,
                             error.warnings[0].path)
            self._assertItemsEqual(candidates,
                                  error.warnings[0].candidates)
