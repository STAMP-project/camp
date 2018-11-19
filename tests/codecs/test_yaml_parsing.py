#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.yaml import YAML
from camp.entities.model import DockerFile, DockerImage, Substitution

from StringIO import StringIO

from unittest import TestCase



class BuiltModelAreComplete(TestCase):


    def setUp(self):
        self._codec = YAML()


    def test_given_a_one_component_stack(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))

        model = self._codec.load_model_from(StringIO(text))
        self._assert_components(model, ["server"])
        self._assert_services(model, ["Wonderful"])
        self._assert_features(model, [])

        server = model.resolve("server")
        self._assert_component_services(server, ["Wonderful"], [])
        self._assert_component_features(server, [], [])
        self._assert_variables(server, [])

        self._assert_goals(model.goals, ["Wonderful"], [])


    def test_given_a_one_component_stack_with_two_variables(self):
        text = ("components:\n"
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
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))

        model = self._codec.load_model_from(StringIO(text))
        self._assert_components(model, ["server"])
        self._assert_services(model, ["Wonderful"])
        self._assert_features(model, [])

        server = model.resolve("server")
        self._assert_component_services(server, ["Wonderful"], [])
        self._assert_component_features(server, [], [])
        self._assert_variables(server, [ ("memory", ["1GB", "2GB"]),
                                         ("threads", [64, 128, 256])])

        self._assert_goals(model.goals, ["Wonderful"], [])


    def test_given_a_two_component_stack(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      requires_features: [ Python27 ]\n"
                "   python:\n"
                "      provides_features: [ Python27 ]\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        Model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))

        model = self._codec.load_model_from(StringIO(text))
        self._assert_components(model, ["server", "python"])
        self._assert_services(model, ["Wonderful"])
        self._assert_features(model, ["Python27"])

        server = model.resolve("server")
        self._assert_component_services(server, ["Wonderful"], [])
        self._assert_component_features(server, [], ["Python27"])
        self._assert_variables(server, [])

        python = model.resolve("python")
        self._assert_component_services(python, [], [])
        self._assert_component_features(python, ["Python27"], [])
        self._assert_variables(python, [])

        self._assert_goals(model.goals, ["Wonderful"], [])


    def test_given_a_component_with_docker_file(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      implementation:\n"
                "         docker:\n"
                "            file: server/Dockerfile\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings),
                        ([str(w) for w in self._codec.warnings])
        )

        model = self._codec.load_model_from(StringIO(text))
        self._assert_components(model, ["server"])
        self._assert_services(model, ["Wonderful"])
        self._assert_features(model, [])

        server = model.resolve("server")
        self._assert_implementation(server, DockerFile("server/Dockerfile"))
        self._assert_component_services(server, ["Wonderful"], [])
        self._assert_component_features(server, [], [])
        self._assert_variables(server, [])

        self._assert_goals(model.goals, ["Wonderful"], [])


    def test_given_a_component_with_a_docker_image(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      implementation:\n"
                "         docker:\n"
                "            image: fchauvel/camp:dev\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings),
                        ([str(w) for w in self._codec.warnings])
        )

        model = self._codec.load_model_from(StringIO(text))
        self._assert_components(model, ["server"])
        self._assert_services(model, ["Wonderful"])
        self._assert_features(model, [])

        server = model.resolve("server")
        self._assert_implementation(server, DockerImage("fchauvel/camp:dev"))
        self._assert_component_services(server, ["Wonderful"], [])
        self._assert_component_features(server, [], [])
        self._assert_variables(server, [])

        self._assert_goals(model.goals, ["Wonderful"], [])


    def test_given_a_component_with_a_realized_variable(self):
        text = ("components:\n"
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
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings),
                        ([str(w) for w in self._codec.warnings]))

        server = model.resolve("server")
        self.assertEqual(server.variables[0].realization,
                        [ Substitution(
                            targets=["file1", "path/to/file2"],
                            pattern="xmem=1GB",
                            replacements=["xmem=1", "xmem=2", "xmem=4"])])
        
    def _assert_components(self, model, names):
        self.assertItemsEqual(names,
                              [each.name for each in model.components])


    def _assert_services(self, model, names):
        self.assertItemsEqual(names,
                              [each.name for each in model.services])


    def _assert_features(self, model, names):
        self.assertItemsEqual(names,
                              [each.name for each in model.features])


    def _assert_component_services(self, component, provided, required):
        self.assertItemsEqual(provided,
                              [each.name for each in component.provided_services])
        self.assertItemsEqual(required,
                              [each.name for each in component.required_services])

    def _assert_component_features(self, component, provided, required):
        self.assertItemsEqual(provided,
                              [each.name for each in component.provided_features])
        self.assertItemsEqual(required,
                              [each.name for each in component.required_features])


    def _assert_implementation(self, component, expected_implementation):
        self.assertEqual(expected_implementation,
                         component.implementation)

    def _assert_variables(self, component, variables):
        self.assertEqual(len(variables), len(component.variables))
        for name, values in variables:
            match = next((variable for variable in component.variables\
                          if variable.name == name),
                         None)
            if match:
                self.assertItemsEqual(match.domain, values)

            else:
                self.fail("Component '%s' lacks variable '%s'." % (component.name, name))


    def _assert_goals(self, goal, services, features):
        self.assertItemsEqual(services,
                              [each.name for each in goal.services])
        self.assertItemsEqual(features,
                              [each.name for each in goal.features])



class IgnoredEntriesAreReported(TestCase):

    def setUp(self):
        self._codec = YAML()


    def test_when_an_extra_entry_is_in_the_root(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "extra: this entry should be reported!\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("extra")

        
    def test_when_an_extra_entry_is_in_a_component(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      extra: this entry should be reported!\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("components/server/extra")
        

    def test_when_an_extra_entry_is_in_the_variables(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      variables:\n"
                "         memory:\n"
                "            extra: this entry should be reported!\n"
                "            values: [ 1GB, 2GB]\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("components/server/variables/memory/extra")

    
    def test_when_an_extra_entry_is_in_a_substitution(self):
        text = ("components:\n"
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
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("components/server/variables/memory/realization/#1/extra")

        

    def test_when_an_extra_entry_is_in_the_implementation(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      implementation:\n"
                "         extra: this entry should be reported!\n"
                "         docker:\n"
                "            file: DockerFile\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("components/server/implementation/extra")
        

    def test_when_an_extra_entry_is_in_the_docker(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      implementation:\n"
                "         docker:\n"
                "            extra: this entry should be reported!\n"
                "            file: DockerFile\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("components/server/implementation/docker/extra")


    def test_when_an_extra_entry_is_in_the_goals(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "goals:\n"
                "   extra: this entry should be reported!\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_extra_is("goals/extra")

    
    def assert_extra_is(self, expected_path):
        self.assertEqual(1, len(self._codec.warnings))
        self.assertEqual(expected_path,
                         self._codec.warnings[0].path)



class TypeMismatchAreReported(TestCase):


    def setUp(self):
        self._codec = YAML()


    def test_with_a_string_as_component(self):
        text = ("components: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("dict", "str", "components")


    def test_with_a_string_as_provided_services(self):
        text = ("components: \n"
                "  server:\n"
                "     provides_services: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list", "str",
                            "components/server/provides_services")


    def test_with_a_string_as_required_services(self):
        text = ("components: \n"
                "  server:\n"
                "     requires_services: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list", "str",
                            "components/server/requires_services")


    def test_with_a_string_as_provided_features(self):
        text = ("components: \n"
                "  server:\n"
                "     provides_features: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list", "str",
                            "components/server/provides_features")


    def test_with_a_string_as_required_features(self):
        text = ("components: \n"
                "  server:\n"
                "     requires_features: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list", "str",
                            "components/server/requires_features")


    def test_with_a_string_as_variables(self):
        text = ("components: \n"
                "  server:\n"
                "     requires_features: [ Awesome ]\n"
                "     variables: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("dict", "str", "components/server/variables")


    def test_with_a_string_as_implementation(self):
        text = ("components: \n"
                "  server:\n"
                "     requires_features: [ Awesome ]\n"
                "     implementation: blablabla\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("dict", "str", "components/server/implementation")


    def test_with_a_string_as_goals(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Awesome ]\n"
                "goals: blablabla\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("dict", "str", "goals")


    def test_with_a_string_as_running(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Awesome ]\n"
                "goals:\n"
                "  running: blablabla\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list", "str", "goals/running")


    def test_with_a_string_as_substitution_replacements(self):
        text = ("components:\n"
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
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list",
                            "str",
                            "components/server/variables/memory/realization/#1/replacements",
                            2)


    def test_with_a_string_as_substitution_targets(self):
        text = ("components:\n"
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
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_warning("list",
                            "str",
                            "components/server/variables/memory/realization/#1/targets",
                            2)



    def assert_warning(self, expected, found, path, warning_count=1):
        self.assertEqual(warning_count, len(self._codec.warnings),
                         [str(w) for w in self._codec.warnings])
        self.assertEqual(path,
                         self._codec.warnings[0].path)
        self.assertEqual(found,
                         self._codec.warnings[0].found)
        self.assertEqual(expected,
                         self._codec.warnings[0].expected)



class TypeMismatchesAreNotReportedWhenStringIsExpected(TestCase):


    def setUp(self):
        self._codec = YAML()


    def test_with_a_boolean_among_running_items(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Awesome ]\n"
                "goals:\n"
                "  running: [ Awesome, True ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_provided_services(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Awesome, 1234.5 ]\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_required_services(self):
        text = ("components:\n"
                "   server:\n"
                "      requires_services: [ Awesome, 1234.5 ]\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_provided_features(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_features: [ Awesome, 1234.5 ]\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_required_services(self):
        text = ("components:\n"
                "   server:\n"
                "      requires_features: [ Awesome, 1234.5 ]\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_variable_values(self):
        text = ("components:\n"
                "   server:\n"
                "      requires_services: [ Awesome ]\n"
                "      variables:\n"
                "         memory:\n"
                "           values: [ High, 1234]\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_docker_file(self):
        text = ("components:\n"
                "   server:\n"
                "      requires_services: [ Awesome ]\n"
                "      implementation:\n"
                "         docker:\n"
                "           file: 1234.5\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))


    def test_with_a_number_among_docker_image(self):
        text = ("components:\n"
                "   server:\n"
                "      requires_services: [ Awesome ]\n"
                "      implementation:\n"
                "         docker:\n"
                "           image: 1234.5\n"
                "goals:\n"
                "  running: [ Awesome ]\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(0, len(self._codec.warnings))



class MissingMandatoryEntriesAreReported(TestCase):


    def setUp(self):
        self._codec = YAML()


    def test_when_omitting_substitution_targets(self):
        text = ("components:\n"
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
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_missing("components/server/variables/memory/realization/#1",
                            ["targets"])


    def test_when_omitting_substitution_pattern(self):
        text = ("components:\n"
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
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_missing("components/server/variables/memory/realization/#1",
                            ["pattern"])
        

    def test_when_omitting_substitution_replacements(self):
        text = ("components:\n"
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
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_missing("components/server/variables/memory/realization/#1",
                            ["replacements"])


    def test_when_omitting_the_docker_file(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      implementation:\n"
                "         docker: {}\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assert_missing("components/server/implementation/docker",
                            ["file", "image"])
        


    def assert_missing(self, path, candidates):
        self.assertEqual(1, len(self._codec.warnings))
        self.assertEqual(path,
                         self._codec.warnings[0].path)
        self.assertItemsEqual(candidates,
                              self._codec.warnings[0].candidates)
        
