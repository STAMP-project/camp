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

from camp.codecs import YAMLCodec
from camp.generate import Z3Problem



class SimplestModelTest(TestCase):


    def setUp(self):
        self._yaml_file = StringIO("components:\n"
                                   "   server:\n"
                                   "      provides_services: [ MyService ]\n"
                                   "      variables:\n"
                                   "         memory:\n"
                                   "           domain:\n"
                                   "             - 1GB\n"
                                   "             - 2GB\n"
                                   "goals:\n"
                                   "   running:\n"
                                   "      - MyService\n")

        self._yaml = YAMLCodec()


    def test_finds_the_only_configuration(self):
        model = self._yaml.load_model_from(self._yaml_file)
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
