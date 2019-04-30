#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Model, Component, Variable, Substitution, \
    DockerFile, Instance, Configuration, Service, Goals
from camp.realize import Builder

from os import makedirs
from os.path import join as join_paths

from tests.util import create_temporary_workspace

from unittest import TestCase



class VariablesRealization(TestCase):


    def setUp(self):
        self._builder = Builder()
        self._workspace = create_temporary_workspace(self.DIRECTORY)
        self.create_docker_file()
        self.create_config_file()
        self.create_docker_compose_file()

    DIRECTORY = "realize/variables"


    def create_docker_file(self):
        directory = join_paths(self._workspace, "template", "server")
        makedirs(directory)
        path = join_paths(directory, "Dockerfile")
        with open(path, "w") as docker_file:
            docker_file.write("FROM debian:jessie\n"
                              "mem=XXX")


    def create_config_file(self):
        path = join_paths(self._workspace, "template", "server", "server.cfg")
        with open(path, "w") as docker_file:
            docker_file.write("mem=XXX")





    def create_docker_compose_file(self):
        path = join_paths(self._workspace, "template", "docker-compose.yml")
        with open(path, "w") as docker_file:
            docker_file.write("mem=XXX")


    def test_succeeds_in_component_files(self):
        model = Model(
            components=[
                Component(name="server",
                          provided_services=[Service("Awesome")],
                          variables=[
                              Variable(
                                  name="memory",
                                  value_type=str,
                                  values=["1GB", "2GB"],
                                  realization=[
                                      Substitution(
                                          targets=["server/Dockerfile",
                                                   "server/server.cfg"],
                                          pattern="mem=XXX",
                                          replacements=["mem=1", "mem=2"])
                                  ])
                          ],
                          implementation=DockerFile("server/Dockerfile"))
            ],
            goals=Goals(services=[Service("Awesome")]))

        server = model.resolve("server")
        configuration = Configuration(
            model,
            instances = [
                Instance(name="server_0",
                         definition=server,
                         configuration=[(server.variables[0], "2GB")])
            ])

        self.realize(configuration)

        self.assert_file_contains("config_1/images/server_0/Dockerfile", "mem=2")
        self.assert_file_contains("config_1/images/server_0/server.cfg", "mem=2")


    def test_succeeds_in_inner_component_files(self):
        """
        See Issue #48, https://github.com/STAMP-project/camp/issues/48
        """
        self._create_inner_configuration_file()
        model = Model(
            components=[
                Component(name="server",
                          provided_services=[Service("Awesome")],
                          variables=[
                              Variable(
                                  name="memory",
                                  value_type=str,
                                  values=["1GB", "2GB"],
                                  realization=[
                                      Substitution(
                                          targets=["server/src/config/settings.ini"],
                                          pattern="parameter=XYZ",
                                          replacements=["parameter=1GB",
                                                        "parameter=2GB"])
                                  ])
                          ],
                          implementation=DockerFile("server/Dockerfile"))
            ],
            goals=Goals(services=[Service("Awesome")]))

        server = model.resolve("server")
        configuration = Configuration(
            model,
            instances = [
                Instance(name="server_0",
                         definition=server,
                         configuration=[(server.variables[0], "2GB")])
            ])

        self.realize(configuration)

        self.assert_file_contains(
            "config_1/images/server_0/src/config/settings.ini",
            "parameter=2GB")


    def _create_inner_configuration_file(self):
        path = join_paths(self._workspace,
                          "template",
                          "server",
                          "src",
                          "config")
        makedirs(path)
        resource = join_paths(path, "settings.ini")
        with open(resource, "w") as config_file:
            config_file.write("parameter=XYZ")


    def test_succeeds_in_orchestration_file(self):
        model = Model(
            components=[
                Component(name="server",
                          provided_services=[Service("Awesome")],
                          variables=[
                              Variable(
                                  name="memory",
                                  value_type=str,
                                  values=["1GB", "2GB"],
                                  realization=[
                                      Substitution(
                                          targets=["docker-compose.yml"],
                                          pattern="mem=XXX",
                                          replacements=["mem=1", "mem=2"])
                                  ])
                          ],
                          implementation=DockerFile("server/Dockerfile"))
            ],
            goals=Goals(services=[Service("Awesome")]))

        server = model.resolve("server")
        configuration = Configuration(
            model,
            instances = [
                Instance(name="server_0",
                         definition=server,
                         configuration=[(server.variables[0], "2GB")])
            ])

        self.realize(configuration)

        self.assert_file_contains("config_1/docker-compose.yml", "mem=2")


    def test_raises_error_when_no_match_if_found_in_target(self):
        """
        See Issue #40
        """
        model = Model(
            components=[
                Component(name="server",
                          provided_services=[Service("Awesome")],
                          variables=[
                              Variable(
                                  name="memory",
                                  value_type=str,
                                  values=["1GB", "2GB"],
                                  realization=[
                                      Substitution(
                                          targets=["docker-compose.yml"],
                                          pattern="pattern that does not exist",
                                          replacements=["mem=1", "mem=2"])
                                  ])
                          ],
                          implementation=DockerFile("server/Dockerfile"))
            ],
            goals=Goals(services=[Service("Awesome")]))

        server = model.resolve("server")
        configuration = Configuration(
            model,
            instances = [
                Instance(name="server_0",
                         definition=server,
                         configuration=[(server.variables[0], "2GB")])
            ])

        with self.assertRaises(Exception):
            self.realize(configuration)


    def realize(self, configuration):
        source = self._workspace
        destination = join_paths(self._workspace, "config_1")
        self._builder.build(configuration, source, destination)


    def assert_file_contains(self, resource, pattern):
        path = join_paths(self._workspace, resource)
        with open(path, "r") as resource_file:
            content = resource_file.read()
            self.assertIn(pattern, content)
