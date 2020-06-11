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
from camp.commands import Command, Generate
from camp.core import Camp
from camp.generate import Z3Problem
from camp.realize import Builder

from os import listdir, makedirs
from os.path import join

from re import match

from tempfile import mkdtemp

from unittest import TestCase


    
class ConfigurationsAreGenerated(TestCase):


    def test_single_component(self):
        self.prepare_sample(
            "\n"
            "components:\n"
            "  server:\n"
            "    provides_services: [ Awesome ]\n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n")

        self.invoke_camp_generate(Generate.ATOMIC)

        self.assert_configuration_count_is(1)


    def test_a_single_variable(self):
        self.prepare_sample(
            "components:\n"
            "  server:\n"
            "    provides_services: [ Awesome ]\n"
            "    variables:\n"
            "      memory:\n"
            "        values: [1GB, 2GB, 4GB]\n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n"
            "        \n")

        self.invoke_camp_generate(Generate.ATOMIC)

        self.assert_configuration_count_is(3)


    def test_two_variables(self):
        self.prepare_sample(
            "components:\n"
            "  server:\n"
            "    provides_services: [ Awesome ]\n"
            "    variables:\n"
            "      memory:\n"
            "        values: [1GB, 2GB, 4GB]\n"
            "      cpu:\n"
            "        values: [1GHz, 2GHz]\n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n"
            "        \n")

        self.invoke_camp_generate(Generate.ATOMIC)

        # Assuming the Reference configuration is (1GB, 1GHz)
        # We expect 4 configs: ref, (1GB, 2GHz), (2GB,  1GHz), (4GB, 1GHz)
        self.assert_configuration_count_is(4)


    def test_two_components_with_one_variable(self):
        self.prepare_sample(
            "components:\n"
            "  server:\n"
            "    provides_services: [ Awesome ]\n"
            "    requires_services: [ Client ]\n"
            "    variables:\n"
            "      memory:\n"
            "        values: [1GB, 2GB, 4GB]\n"
            "  client:\n"
            "    provides_services: [ Client ]\n"
            "    variables:\n"
            "      cpu:\n"
            "        values: [1GHz, 2GHz]\n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n"
            "        \n")

        self.invoke_camp_generate(Generate.ATOMIC)

        # Assuming the Reference configuration is (1GB, 1GHz)
        # We expect 4 configs: ref, (1GB, 2GHz), (2GB,  1GHz), (4GB, 1GHz)
        self.assert_configuration_count_is(4)


    def prepare_sample(self, sample):
        self._working_directory = join(mkdtemp(prefix="camp_"), "generate")
        makedirs(self._working_directory)
        with open(join(self._working_directory, "camp.yaml"), "w") as stream:
            stream.write(sample)


    def invoke_camp_generate(self, mode=Generate.ALL):
        camp = Camp(YAML(), Z3Problem, Builder())
        command = Command.extract_from(["generate", "--mode", mode, "-d", self._working_directory])
        command.send_to(camp)


    def assert_configuration_count_is(self, expected):
        generated = []
        destination = join(self._working_directory, "out")
        for each_file in listdir(destination):
            if match(r"config_\d+", each_file):
                generated.append(each_file)
        self.assertEqual(expected, len(generated), str(generated))
