#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.yaml import YAML
from camp.generate import Z3Problem

from StringIO import StringIO

from unittest import TestCase



class VariablesAreAssigned(TestCase):

    def setUp(self):
        self._yaml = YAML()


    def assert_variables_values(self, text, configuration_count, expected_values):
        model = self._yaml.load_model_from(StringIO(text))

        self.assertFalse(self._yaml.warnings, "\n".join(str(each) for each in self._yaml.warnings))

        solver = Z3Problem.from_model(model)
        configurations = list(solver.all_solutions())

        self.assertEqual(configuration_count, len(configurations))

        actual_values = { key: [] for key in expected_values }
        for each_configuration in configurations:
            for each_instance in each_configuration.instances:
                for variable, value in each_instance.configuration:
                    if variable.name not in actual_values:
                        actual_values[variable.name] = []
                    actual_values[variable.name].append(value)

        self.assertEqual(len(expected_values),
                         len(actual_values))

        for each_variable in expected_values:
            self.assertEqual(set(expected_values[each_variable]),
                             set(actual_values[each_variable]))


    def test_given_integer_variables(self):
        self.assert_variables_values(
            "components:\n"
            "   server:\n"
            "      provides_services: [ MyService ]\n"
            "      variables:\n"
            "         memory:\n"
            "            type: Integer\n"
            "         max_thread:\n"
            "            type: Integer\n"
            "constraints:\n"
            "    - CInstance.forall(ci, ci.configuration.exists(val, And([val.variable == variable('server', 'memory'), val.value == 4])))\n"
            "    - CInstance.forall(ci, ci.configuration.exists(val1, And([val1.variable == variable('server', 'max_thread'), ci.configuration.exists(val2, And([val2.variable == variable('server', 'memory'), val1.value * 2 == val2.value]))])))\n"
            "goals:\n"
            "   running: \n"
            "     - MyService \n",
            configuration_count=1,
            expected_values={"memory": [4],
                             "max_thread": [2]})


    def test_given_enumerated_variables(self):
        self.assert_variables_values(
            "components:\n"
            "   server:\n"
            "      provides_services: [ MyService ]\n"
            "      variables:\n"
            "         memory:\n"
            "           type: Symbols\n"
            "           values: [ 1GB, 2GB ]\n"
            "goals:\n"
            "   running:\n"
            "      - MyService\n",
            configuration_count=2,
            expected_values={"memory": ["1GB", "2GB"]})


    def test_given_enumerated_integer_variables(self):
        self.assert_variables_values(
            "components:\n"
            "   server:\n"
            "      provides_services: [ MyService ]\n"
            "      variables:\n"
            "         memory:\n"
            "           type: Integer\n"
            "           values: [ 5, 10 ]\n"
            "goals:\n"
            "   running:\n"
            "      - MyService\n",
            configuration_count=2,
            expected_values={"memory": [5, 10]})


    def test_given_covered_integer_variables(self):
        self.assert_variables_values(
            "components:\n"
            "   server:\n"
            "      provides_services: [ MyService ]\n"
            "      variables:\n"
            "         memory:\n"
            "           type: Integer\n"
            "           values: \n"
            "             range: [100, 200]\n"
            "             coverage: 50\n"
            "goals:\n"
            "   running:\n"
            "      - MyService\n",
            configuration_count=3,
            expected_values={ "memory": [100, 150, 200]})
