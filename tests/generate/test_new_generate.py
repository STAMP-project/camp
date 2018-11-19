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
from camp.generate import Z3Problem

from StringIO import StringIO

from sys import stdout

from unittest import TestCase



class VariablesAreAssigned(TestCase):

    def setUp(self):
        self._yaml = YAML()


    def test_given_integer_variables(self):
        model = self._yaml.load_model_from(StringIO(
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
            "     - MyService \n"))
        
        self.assertFalse(self._yaml.warnings, "\n".join(str(each) for each in self._yaml.warnings))
        
        solver = Z3Problem.from_model(model)
        configurations = list(solver.all_solutions())

        self.assertEqual(1, len(configurations))

        self.assertTrue(
            all(each.instances[0].definition is model.resolve("server") \
                for each in configurations))

        self.assertEqual(4, configurations[0].instances[0]["memory"])
        self.assertEqual(2, configurations[0].instances[0]["max_thread"])


    def test_given_enumerated_variables(self):
        model = self._yaml.load_model_from(StringIO(
            "components:\n"
            "   server:\n"
            "      provides_services: [ MyService ]\n"
            "      variables:\n"
            "         memory:\n"
            "           type: Symbols\n"
            "           values: [ 1GB, 2GB ]\n"
            "goals:\n"
            "   running:\n"
            "      - MyService\n"))

        
        self.assertFalse(self._yaml.warnings, "\n".join(str(each) for each in self._yaml.warnings))

        solver = Z3Problem.from_model(model)
        configurations = list(solver.all_solutions())

        self.assertEqual(2, len(configurations))
        self.assertTrue(
            all(each.instance_count == 1 for each in configurations))
        self.assertTrue(
            all(each.instances[0].definition is model.resolve("server") \
                for each in configurations))
        self.assertTrue(
            all(any(value in [x[1] for x in conf.instances[0].configuration] for conf in configurations)
                for value in ["1GB", "2GB"]))


    def test_given_enumerated_integer_variables(self):
        model = self._yaml.load_model_from(StringIO(
            "components:\n"
            "   server:\n"
            "      provides_services: [ MyService ]\n"
            "      variables:\n"
            "         memory:\n"
            "           type: Integer\n"
            "           values: [ 5, 10 ]\n"
            "goals:\n"
            "   running:\n"
            "      - MyService\n"))

        
        self.assertFalse(self._yaml.warnings, "\n".join(str(each) for each in self._yaml.warnings))

        solver = Z3Problem.from_model(model)
        configurations = list(solver.all_solutions())
        
        self.assertEqual(2, len(configurations))

        self.assertTrue(
            all(each.instances[0].definition is model.resolve("server") \
                for each in configurations))

        memory_sizes = [each_configuration.instances[0]["memory"] \
                    for each_configuration in configurations]
        self.assertEqual(set(memory_sizes), set([5, 10]))

        


    def test_given_covered_integer_variables(self):
        model = self._yaml.load_model_from(StringIO(
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
            "      - MyService\n"))

        
        self.assertFalse(self._yaml.warnings, "\n".join(str(each) for each in self._yaml.warnings))

        solver = Z3Problem.from_model(model)
        configurations = list(solver.all_solutions())
        
        self.assertEqual(3, len(configurations))

        self.assertTrue(
            all(each.instances[0].definition is model.resolve("server") \
                for each in configurations))

        memory_sizes = [each_configuration.instances[0]["memory"] \
                    for each_configuration in configurations]
        self.assertEqual(set(memory_sizes), set([100, 150, 200]))
