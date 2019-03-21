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
from camp.commands import Command
from camp.core import Camp
from camp.generate import Z3Problem
from camp.realize import Builder

from os import listdir, makedirs
from os.path import join, isdir

from re import match

from shutil import rmtree

from unittest import TestCase



class FilesAreGenerated(TestCase):


    def test_single_component(self):
        self.prepare_sample(
            "\n"
            "components:\n"
            "  server:\n"
            "    provides_services: [ Awesome ]\n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n")

        self.invoke_camp_generate()

        self.assert_configuration_count_is(1)


    def test_variables(self):
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

        self.invoke_camp_generate()

        self.assert_configuration_count_is(3)


    def test_stack(self):
        self.prepare_sample(
            "components:\n"
            "  app:\n"
            "    provides_services: [ Awesome ]\n"
            "    requires_features: [ JRE ]\n"
            "  jre:\n"
            "    provides_features: [ JRE ]\n"
            "    variables:\n"
            "      version:\n"
            "        values: [v7, v8]\n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n")

        self.invoke_camp_generate()

        self.assert_configuration_count_is(2)


    def test_orchestrations(self):
        self.prepare_sample(
            "components:\n"
            "  app:\n"
            "    provides_services: [ Awesome ]\n"
            "    requires_services: [ DB ]\n"
            "    requires_features: [ JRE ]\n"
            "  jre:\n"
            "    provides_features: [ JRE ]\n"
            "  mysql:\n"
            "    provides_services: [ DB ]\n"
            "  postgresql:\n"
            "    provides_services: [ DB ]\n"
            "    \n"
            "goals:\n"
            "  running:\n"
            "    - Awesome\n")

        self.invoke_camp_generate()

        self.assert_configuration_count_is(2)


    def prepare_sample(self, sample):
        self._working_directory = self.WORKING_DIRECTORY
        if isdir(self._working_directory):
            rmtree(self._working_directory)
        makedirs(self._working_directory)
        with open(join(self._working_directory, "camp.yaml"), "w") as stream:
            stream.write(sample)

    WORKING_DIRECTORY = "tmp/generate"


    def invoke_camp_generate(self):
        camp = Camp(YAML(), Z3Problem, Builder())
        command = Command.extract_from(["generate", "--all", "-d", self._working_directory])
        command.send_to(camp)


    def assert_configuration_count_is(self, expected):
        generated = []
        destination = join(self.WORKING_DIRECTORY, "out")
        for each_file in listdir(destination):
            if match(r"config_\d+", each_file):
                generated.append(each_file)
        self.assertEqual(expected, len(generated), str(generated))
