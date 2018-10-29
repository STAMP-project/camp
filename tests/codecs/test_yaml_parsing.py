#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from unittest import TestCase

from StringIO import StringIO
from pprint import pprint


from camp.codecs import YAMLCodec



class BuiltModelAreComplete(TestCase):


    def setUp(self):
        self._codec = YAMLCodec()


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
                "          domain: [1GB, 2GB]\n"
                "        threads:\n"
                "          domain: [64, 128, 256]\n"
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
                                         ("threads", ["64", "128", "256"])])

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

    

class IgnoredEntryAreReported(TestCase):

    def setUp(self):
        self._codec = YAMLCodec()


    def test_when_an_extra_entry_is_in_the_root(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "extra: this should not be there!\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(1, len(self._codec.warnings))
        self.assertEqual("extra",
                         self._codec.warnings[0].path)


    def test_when_an_extra_entry_is_in_a_component(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "      extra: this should not be there!\n"
                "goals:\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(1, len(self._codec.warnings))
        self.assertEqual("components/server/extra",
                         self._codec.warnings[0].path)


    def test_when_an_extra_entry_is_in_the_goals(self):
        text = ("components:\n"
                "   server:\n"
                "      provides_services: [ Wonderful ]\n"
                "goals:\n"
                "   extra: this should not be there!\n"
                "   running:\n"
                "      - Wonderful\n")

        model = self._codec.load_model_from(StringIO(text))

        self.assertEqual(1, len(self._codec.warnings))
        self.assertEqual("goals/extra",
                         self._codec.warnings[0].path)
