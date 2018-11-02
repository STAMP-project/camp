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
from camp.core import Camp
from camp.generate import Z3Problem
from camp.realize import Builder
from camp.run import Runner

from os import makedirs
from os.path import isfile, exists, isdir, join as join_paths

from shutil import rmtree

from unittest import TestCase



class AllYAMLConfigurationsAreBuilt(TestCase):


    def setUp(self):
        self._prepare_input_directory()
        self._prepare_output_directory()


    def _prepare_input_directory(self):
        self._create_or_clean(self.INPUT_DIRECTORY)
        self._create_model()
        self._create_docker_file()

    INPUT_DIRECTORY = "temp/realize/configs"


    @staticmethod
    def _create_or_clean(directory):
        if isdir(directory):
            rmtree(directory)
        makedirs(directory)


    def _create_model(self):
        path = join_paths(self.INPUT_DIRECTORY, "model.yml")
        with open(path, "w") as model:
            model.write(
                "components:\n"
                "  server:\n"
                "    provides_services: [ Awesome ]\n"
                "    variables:\n"
                "       memory:\n"
                "         domain: [ 1GB, 2GB ]\n"
                "         realization:\n"
                "            - targets: [ server/Dockerfile ]\n"
                "              pattern: mem=XXX\n"
                "              replacements: [ mem=1, mem=2 ]\n"
                "    implementation:\n"
                "      docker:\n"
                "        file: server/Dockerfile\n"
                "goals:\n"
                "   running: [ Awesome ]\n")


    def _create_docker_file(self):
        directory = join_paths(self.INPUT_DIRECTORY, "server")
        makedirs(directory)
        path = join_paths(directory, "Dockerfile")
        with open(path, "w") as docker_file:
            docker_file.write("FROM debian:jessie\n"
                              "mem=XXX")


    def _prepare_output_directory(self):
        self._create_configuration_1()
        self._create_configuration_2()


    def _create_configuration_1(self):
        directory = join_paths(self.OUTPUT_DIRECTORY, "config_1")
        makedirs(directory)
        path = join_paths(directory, "configuration.yml")
        with open(path, "w") as configuration_1:
            configuration_1.write(
                "instances:\n"
                "  server_0:\n"
                "    name: server_0\n"
                "    definition: server\n"
                "    feature_provider: null\n"
                "    services_providers: []\n"
                "    configuration:\n"
                "       memory: 1GB\n")

    OUTPUT_DIRECTORY = "temp/realize/configs/out"


    def _create_configuration_2(self):
        directory = join_paths(self.OUTPUT_DIRECTORY, "config_2")
        makedirs(directory)
        path = join_paths(directory, "configuration.yml")
        with open(path, "w") as configuration_1:
            configuration_1.write(
                "instances:\n"
                "  server_0:\n"
                "    name: server_0\n"
                "    definition: server\n"
                "    feature_provider: null\n"
                "    services_providers: []\n"
                "    configuration:\n"
                "       memory: 2GB\n")



    def test_with_two_configurations(self):
        self.realize()

        self.assert_generated("config_1/images/server_0/Dockerfile",
                              "config_2/images/server_0/Dockerfile")



    def realize(self):
        runner = Runner(Camp(YAML(),
                             Z3Problem,
                             Builder()))
        runner.start(["realize", "-d", self.INPUT_DIRECTORY,
                      "-o", self.OUTPUT_DIRECTORY])



    def assert_generated(self, *files):
        for each_file in files:
            path = join_paths(self.OUTPUT_DIRECTORY, each_file)
            self.assertTrue(exists(path),
                            "Missing file '%s'" % each_file)
