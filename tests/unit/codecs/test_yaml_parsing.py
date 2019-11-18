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

from camp.codecs.yaml import YAML
from camp.entities.model import DockerFile, DockerImage, Substitution, \
    TestSettings, ResourceSelection, ComponentResourceSelection
from camp.entities.report import SuccessfulTest, FailedTest, ErroneousTest, \
    TestSuite, TestReport

from unittest import TestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class BuiltModelAreComplete(TestCase):


    def setUp(self):
        self._codec = YAML()


    def _assertItemsEqual(self, expected, actual):
        # For compatibility with Python 2.7, as the method
        # assertItemsEquals has been renamed in Python 3.3 into
        # 'assertCountEqual'.
        return self.assertEqual(sorted(expected), sorted(actual))


    def test_given_a_one_component_stack(self):
        self.assert_complete("components:\n"
                             "   server:\n"
                             "      provides_services: [ Wonderful ]\n"
                             "goals:\n"
                             "   running:\n"
                             "      - Wonderful\n",
                             expectations={
                                 "services": ["Wonderful"],
                                 "features": [],
                                 "components" : {
                                     "server": {
                                         "provided_services": ["Wonderful"],
                                         "required_services": [],
                                         "provided_features": [],
                                         "required_features": [],
                                         "implementation": None,
                                         "variables": {}
                                     }
                                 },
                                 "goals": {
                                     "services": ["Wonderful"],
                                     "features": []}
                             })


    def test_given_a_one_component_stack_with_two_variables(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      variables:\n"
            "        memory:\n"
            "          type: Integer\n"
            "          values: [1GB, 2GB]\n"
            "        threads:\n"
            "          type: Integer\n"
            "          values: [64, 128, 256]\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
            "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": None,
                        "variables": {
                            "threads": {
                                "values": [64, 128, 256],
                                "realization": []
                            },
                            "memory": {
                                "values": ["1GB", "2GB"],
                                "realization": []
                            }
                        }
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })



    def test_given_a_two_component_stack(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      requires_features: [ Python27 ]\n"
            "   python:\n"
            "      provides_features: [ Python27 ]\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": ["Python27"],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": ["Python27"],
                        "implementation": None,
                        "variables": {}
                    },
                    "python": {
                        "provided_services": [],
                        "required_services": [],
                        "provided_features": ["Python27"],
                        "required_features": [],
                        "implementation": None,
                        "variables": {}

                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })


    def test_given_a_component_with_docker_file(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      implementation:\n"
            "         docker:\n"
            "            file: server/Dockerfile\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": DockerFile("server/Dockerfile"),
                        "variables": {}
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })


    def test_given_a_component_with_a_docker_image(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      implementation:\n"
            "         docker:\n"
            "            image: fchauvel/camp:dev\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": DockerImage("fchauvel/camp:dev"),
                        "variables": {}
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })


    def test_given_a_component_with_a_variable_with_substitution(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      variables:\n"
            "        memory:\n"
            "          type: Text\n"
            "          values: [1GB, 2GB, 4GB]\n"
            "          realization:\n"
            "             - targets: [ file1, path/to/file2 ]\n"
            "               pattern: xmem=1GB\n"
            "               replacements: [xmem=1, xmem=2, xmem=4]\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": None,
                        "variables": {
                            "memory": {
                                "values": ["1GB", "2GB", "4GB"],
                                "realization": [
                                    Substitution(
                                        targets=["file1", "path/to/file2"],
                                        pattern="xmem=1GB",
                                        replacements=["xmem=1", "xmem=2", "xmem=4"])
                                ]
                            }
                        }
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })



    def test_given_a_component_with_a_variable_with_resource_selection(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      variables:\n"
            "        memory:\n"
            "          type: Text\n"
            "          values: [apache, nginx]\n"
            "          realization:\n"
            "             - select: \n"
            "                - apache_config.ini\n"
            "                - nginx_config.ini\n"
            "               as: config.ini\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": None,
                        "variables": {
                            "memory": {
                                "values": ["apache", "nginx" ],
                                "realization": [
                                    ResourceSelection(
                                        "config.ini",
                                        ["apache_config.ini", "nginx_config.ini"])
                                ]
                            }
                        }
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })



    def test_given_a_component_containing_tests(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      tests:\n"
            "        command: mvn -B test -gs ./settings.xml\n"
            "        reports:\n"
            "          format: JUnit\n"
            "          location: target/surefire-reports\n"
            "          pattern: TEST*.xml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": None,
                        "variables": {},
                        "tests": TestSettings("mvn -B test -gs ./settings.xml",
                                              "JUnit",
                                              "target/surefire-reports",
                                              "TEST*.xml")
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })



    def test_given_a_component_containing_tests_with_liveness_check(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      tests:\n"
            "        command: mvn -B test -gs ./settings.xml\n"
            "        liveness_test: This is a nice test!\n"
            "        reports:\n"
            "          format: JUnit\n"
            "          location: target/surefire-reports\n"
            "          pattern: TEST*.xml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": None,
                        "variables": {},
                        "tests": TestSettings("mvn -B test -gs ./settings.xml",
                                              "JUnit",
                                              "target/surefire-reports",
                                              "TEST*.xml",
                                              "This is a nice test!")
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })



    def test_given_a_component_with_realization(self):
        self.assert_complete(
            "components:\n"
            "   server:\n"
            "      provides_services: [ Wonderful ]\n"
            "      realization:\n"
            "        - select: apache_docker-compose.yml\n"
            "          instead_of:\n"
            "           - nginx_docker-compose.yml\n"
            "          as: docker-compose.yml\n"
            "goals:\n"
            "   running:\n"
            "      - Wonderful\n",
            expectations={
                "services": ["Wonderful"],
                "features": [],
                "components" : {
                    "server": {
                        "provided_services": ["Wonderful"],
                        "required_services": [],
                        "provided_features": [],
                        "required_features": [],
                        "implementation": None,
                        "variables": {},
                        "realization": [
                            ComponentResourceSelection(
                                "apache_docker-compose.yml",
                                ["nginx_docker-compose.yml"],
                                "docker-compose.yml")
                        ]
                    }
                },
                "goals": {
                    "services": ["Wonderful"],
                    "features": []
                }
            })



    def assert_complete(self, text, expectations):
        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))

        self.assert_goals(model.goals, expectations["goals"])

        self._assertItemsEqual(expectations["services"],
                              [each.name for each in model.services])

        self._assertItemsEqual(expectations["features"],
                              [each.name for each in model.features])

        self.assertEqual(
            set([each.name for each in model.components]),
            set(expectations["components"].keys()))

        for each_component in model.components:
            expectation = expectations["components"][each_component.name]
            self.assert_component(each_component, expectation)


    def assert_goals(self, goals, expectations):
        self._assertItemsEqual(expectations["services"],
                              [each.name for each in goals.services])
        self._assertItemsEqual(expectations["features"],
                              [each.name for each in goals.features])


    def assert_component(self, component, expectation):
        self._assertItemsEqual(
            expectation["provided_services"],
            [each.name for each in component.provided_services])
        self._assertItemsEqual(
            expectation["required_services"],
            [each.name for each in component.required_services])
        self._assertItemsEqual(
            expectation["provided_features"],
            [each.name for each in component.provided_features])
        self._assertItemsEqual(
            expectation["required_features"],
            [each.name for each in component.required_features])
        self.assertEqual(expectation["implementation"],
                         component.implementation)
        self.assert_variables(component, expectation["variables"])
        if "tests" in expectation:
            self.assertEqual(expectation["tests"],
                             component.test_settings)
        if "realization" in expectation:
            self._assertItemsEqual(expectation["realization"],
                                  component.realization)


    def assert_variables(self, component, variables):
        self.assertEqual(len(variables), len(component.variables))
        for name, variable in variables.items():
            match = next((variable for variable in component.variables\
                          if variable.name == name),
                         None)
            if match:
                self._assertItemsEqual(match.domain, variable["values"])
                self._assertItemsEqual(match.realization, variable["realization"])

            else:
                self.fail("Component '%s' lacks variable '%s'." % (component.name, name))



class TestReportsAreSerialized(TestCase):


    def setUp(self):
        self._output = StringIO()
        self._codec = YAML()


    def test_when_it_includes_a_successful_test(self):
        reports = [TestReport("out/config_1", SuccessfulTest("Test 1"))]

        self._codec.save_test_reports(reports, self._output)

        self.assertIn("out/config_1", self._output.getvalue())
        self.assertIn("identifier: Test 1", self._output.getvalue())
        self.assertIn("verdict: 1", self._output.getvalue())


    def test_when_it_includes_a_failed_test(self):
        reports = [TestReport("out/config_1",
                              FailedTest("Test 1", "What a failure!"))]

        self._codec.save_test_reports(reports, self._output)

        self.assertIn("out/config_1", self._output.getvalue())
        self.assertIn("identifier: Test 1", self._output.getvalue())
        self.assertIn("verdict: 2", self._output.getvalue())
        self.assertIn("failure: What a failure!", self._output.getvalue())


    def test_when_it_includes_an_erroneous_test(self):
        reports = [TestReport("out/config_1",
                              ErroneousTest("Test 1", "What an error!"))]

        self._codec.save_test_reports(reports, self._output)

        self.assertIn("out/config_1", self._output.getvalue())
        self.assertIn("identifier: Test 1", self._output.getvalue())
        self.assertIn("verdict: 3", self._output.getvalue())
        self.assertIn("error: What an error!", self._output.getvalue())


    def test_when_it_includes_a_test_suite(self):
        reports = [
            TestReport("out/config_1",
                       TestSuite("Test Suite 1",
                                 SuccessfulTest("Test 1"),
                                 ErroneousTest("Test 2", "What an error!")
                       ))
        ]

        self._codec.save_test_reports(reports, self._output)

        self.assertIn("out/config_1", self._output.getvalue())
        self.assertIn("Test Suite 1", self._output.getvalue())
        self.assertIn("identifier: Test 1", self._output.getvalue())
        self.assertIn("verdict: 1", self._output.getvalue())
        self.assertIn("identifier: Test 2", self._output.getvalue())
        self.assertIn("verdict: 3", self._output.getvalue())
        self.assertIn("error: What an error!", self._output.getvalue())


    def test_when_it_includes_several_reports(self):
        reports = [
            TestReport("out/config_1", SuccessfulTest("Test 1")),
            TestReport("out/config_2", ErroneousTest("Test 1",
                                                     "What an error!"))
        ]

        self._codec.save_test_reports(reports, self._output)
        self.assertIn("out/config_1", self._output.getvalue())
        self.assertIn("identifier: Test 1", self._output.getvalue())
        self.assertIn("verdict: 1", self._output.getvalue())
        self.assertIn("out/config_2", self._output.getvalue())
        self.assertIn("identifier: Test 1", self._output.getvalue())
        self.assertIn("verdict: 3", self._output.getvalue())
        self.assertIn("error: What an error!", self._output.getvalue())
