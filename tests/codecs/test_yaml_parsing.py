#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.yaml import YAML, InvalidYAMLModel
from camp.entities.model import DockerFile, DockerImage, Substitution

from StringIO import StringIO

from unittest import TestCase



class BuiltModelAreComplete(TestCase):


    def setUp(self):
        self._codec = YAML()



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


    def test_given_a_component_with_a_realized_variable(self):
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



    def assert_complete(self, text, expectations):
        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))

        self.assert_goals(model.goals, expectations["goals"])

        self.assertItemsEqual(expectations["services"],
                              [each.name for each in model.services])

        self.assertItemsEqual(expectations["features"],
                              [each.name for each in model.features])

        self.assertEqual(
            set([each.name for each in model.components]),
            set(expectations["components"].keys()))

        for each_component in model.components:
            expectation = expectations["components"][each_component.name]
            self.assert_component(each_component, expectation)


    def assert_goals(self, goals, expectations):
        self.assertItemsEqual(expectations["services"],
                              [each.name for each in goals.services])
        self.assertItemsEqual(expectations["features"],
                              [each.name for each in goals.features])


    def assert_component(self, component, expectation):
        self.assertItemsEqual(
            expectation["provided_services"],
            [each.name for each in component.provided_services])
        self.assertItemsEqual(
            expectation["required_services"],
            [each.name for each in component.required_services])
        self.assertItemsEqual(
            expectation["provided_features"],
            [each.name for each in component.provided_features])
        self.assertItemsEqual(
            expectation["required_features"],
            [each.name for each in component.required_features])
        self.assertEqual(expectation["implementation"],
                         component.implementation)
        self.assert_variables(component, expectation["variables"])


    def assert_variables(self, component, variables):
        self.assertEqual(len(variables), len(component.variables))
        for name, variable in variables.items():
            match = next((variable for variable in component.variables\
                          if variable.name == name),
                         None)
            if match:
                self.assertItemsEqual(match.domain, variable["values"])
                self.assertItemsEqual(match.realization, variable["realization"])

            else:
                self.fail("Component '%s' lacks variable '%s'." % (component.name, name))





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


    def test_when_an_extra_entry_is_in_the_docker(self):
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


    def assert_missing(self, text, path, candidates):
        try:
            model = self._codec.load_model_from(StringIO(text))
            self.fail("InvalidYAMLModel should have been thrown!")

        except InvalidYAMLModel as error:
            self.assertEqual(1, len(error.warnings))
            self.assertEqual(path,
                             error.warnings[0].path)
            self.assertItemsEqual(candidates,
                                  error.warnings[0].candidates)
