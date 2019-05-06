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
    DockerFile, Instance, Configuration, Service, Goals, ResourceSelection, \
    RenameResource
from camp.realize import Builder

from os import makedirs
from os.path import dirname, isfile, join as join_paths

from tests.util import create_temporary_workspace

from unittest import TestCase



class Realization(TestCase):


    def setUp(self):
        self._builder = Builder()
        self._workspace = create_temporary_workspace(self.DIRECTORY)
        self.create_template_file(
            component="server",
            resource="Dockerfile",
            content=("FROM debian:jessie\n"
                     "mem=XXX"))
        self.create_template_file()
        self.create_template_file(
            component="",
            resource="docker-compose.yml",
            content="mem=XXX")


    DIRECTORY = "realize/variables"


    def create_template_file(self,
                           component="server",
                           resource="server.cfg",
                           content="mem=XXX"):
        resource = join_paths(self._workspace, "template", component, resource)
        directory = dirname(resource)
        makedirs(directory, exist_ok=True)
        with open(resource, "w") as resource_file:
            resource_file.write(content)


    def test_select_a_specifc_resource(self):
        self.create_template_file(component="server",
                                  resource="apache_config.ini")
        self.create_template_file(component="server",
                                  resource="nginx_config.json")

        model = Model(
            components=[
                Component(name="server",
                          provided_services=[Service("Awesome")],
                          variables=[
                              Variable(
                                  name="provider",
                                  value_type=str,
                                  values=["apache", "nginx"],
                                  realization=[
                                      ResourceSelection(
                                          "server/apache_config.ini",
                                          "server/nginx_config.json"
                                      )
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
                         configuration=[(server.variables[0], "nginx")])
            ])

        self.realize(configuration)

        self.assert_exists("config_1/images/server_0/nginx_config.json")
        self.assert_does_not_exist("config_1/images/server_0/apache_config.ini")


    def test_rename_a_specifc_resource(self):
        self.create_template_file(component="server",
                                  resource="apache_config.ini")

        model = Model(
            components=[
                Component(name="server",
                          provided_services=[Service("Awesome")],
                          variables=[
                              Variable(
                                  name="provider",
                                  value_type=str,
                                  values=["apache", "nginx"],
                                  realization=[
                                      RenameResource(
                                          "server/apache_config.ini",
                                          "server/config.json"
                                      )
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
                         configuration=[(server.variables[0], "nginx")])
            ])

        self.realize(configuration)

        self.assert_exists("config_1/images/server_0/config.json")
        self.assert_does_not_exist("config_1/images/server_0/apache_config.ini")


    def test_substitute_in_component_files(self):
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


    def test_substitute_pattern_that_contains_regex_sensitive_character(self):
        """
        See Issue #56
        """
        self.create_template_file(content="\"resolve\": \"^1.1.6\"")
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
                                          targets=["server/server.cfg"],
                                          pattern="\"resolve\": \"^1.1.6\"",
                                          replacements=["\"resolve\": 1",
                                                        "\"resolve\": 2"])
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
            "config_1/images/server_0/server.cfg",
            "\"resolve\": 2")


    def test_succeeds_in_inner_component_files(self):
        """
        See Issue #48
        """
        self.create_template_file(
            component="server",
            resource="src/config/settings.ini",
            content="parameter=XYZ")

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


    def assert_exists(self, resource):
        path = join_paths(self._workspace, resource)
        self.assertTrue(isfile(path))


    def assert_does_not_exist(self, resource):
        path = join_paths(self._workspace, resource)
        self.assertFalse(isfile(path))
