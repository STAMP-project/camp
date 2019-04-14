#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.directories import InputDirectory, OutputDirectory
from camp.entities.model import Model, Component, Goals, Configuration, \
    Instance, Service, Feature, DockerImage, DockerFile
from camp.realize import Builder

from os import makedirs
from os.path import isdir, join as join_paths

from re import search

from tests.util import create_temporary_workspace

from unittest import TestCase



class BuilderTest(TestCase):


    def setUp(self):
        self._workspace = create_temporary_workspace(self.WORKING_DIRECTORY)

        self._input = InputDirectory(self._workspace)
        self._output = OutputDirectory(self._workspace + "/out")

        self._input.create_template_file("server",
                                         "Dockerfile",
                                         self.DOCKER_FILE)
        self._input.create_template_file("jdk",
                                         "Dockerfile",
                                         self.DOCKER_FILE)

        self._builder = Builder()

    WORKING_DIRECTORY = "realize/docker"

    DOCKER_FILE = ("FROM openjdk:8-jre\n"
                   "RUN echo this is nice\n")


    def build(self, configuration):
        destination = join_paths(self._workspace, "out/config_0")
        self._builder.build(configuration, self._workspace, destination)


    def assert_directory_structure(self, expected_components):
        self.assertTrue(isdir(self.image_directory), "No image directory!")
        self.assertItemsEqual(expected_components,
                              self.generated_components())



    def assert_generated(self, file_path, with_patterns):
        self.assertTrue(
            self._output.has_file(file_path),
            "Missing file '%s'!" % file_path)
        content = self._output.content_of(file_path)
        for each_pattern in with_patterns:
            if not search(each_pattern, content):
                self.fail("The file '%s' does not contains pattern '%s'!\n"
                          "Content is %s" % (file_path, each_pattern, content))

    def assert_no_image_generated(self, config_index):
        self.assertEqual(0,
                         len(self._output.images_generated_for(config_index)))



class BuildImagesIsGenerated(BuilderTest):


    def test_when_a_component_is_implemented_by_a_docker_file(self):
        model = Model(
            [
                Component("server",
                          provided_services=[Service("Awesome")],
                          required_features=[Feature("JDK")],
                          implementation=DockerFile("server/Dockerfile")),
                Component("jdk",
                          provided_features=[Feature("JDK")],
                          implementation=DockerFile("jdk/Dockerfile"))

            ],
            Goals(services=[Service("Awesome")])
        )

        server_0 = Instance("server_0", model.resolve("server"))
        jdk_0 = Instance("jdk_0", model.resolve("jdk"))

        server_0.feature_provider = jdk_0
        configuration = Configuration(model, [server_0, jdk_0])

        self.build(configuration)

        self.assert_generated(
            "config_0/images/build_images.sh",
             with_patterns=[
                 "docker build -t camp-server_0 ./server",
                 "docker build -t camp-jdk_0 ./jdk_0"
                 ])



class DockerFileGenerated(BuilderTest):

    def test_when_a_component_is_implemented_by_a_docker_file(self):
        model = Model(
            [
                Component("server",
                          provided_services=[Service("Awesome")],
                          implementation=DockerFile("server/Dockerfile"))
            ],
            Goals(services=[Service("Awesome")])
        )

        instance = Instance("server_0", model.resolve("server"))
        configuration = Configuration(model, [instance])

        self.build(configuration)

        self.assert_generated(
            "config_0/images/server_0/Dockerfile",
            with_patterns=[
                "FROM openjdk:8-jre"
            ])


    def test_when_a_component_host_is_implemented_by_a_docker_image(self):
        model = Model(
            [
                Component("server",
                          provided_services=[Service("Awesome")],
                          required_features=[Feature("JDK")],
                          implementation=DockerFile("server/Dockerfile")),
                Component("jdk",
                          provided_features=[Feature("JDK")],
                          implementation=DockerImage("fchauvel/test:1.0.1")),
            ],
            Goals(services=[Service("Awesome")])
        )

        server_0 = Instance("server_0", model.resolve("server"))
        jdk_0 = Instance("jdk_0", model.resolve("jdk"))
        server_0.feature_provider = jdk_0

        configuration = Configuration( model, [ server_0,
                                                jdk_0 ])
        self.build(configuration)

        self.assert_generated(
            "config_0/images/server_0/Dockerfile",
            with_patterns=[
                "FROM fchauvel/test:1.0.1"
            ])


    def test_when_a_component_host_is_implemented_by_a_docker_file(self):
        model = Model(
            [
                Component("server",
                          provided_services=[Service("Awesome")],
                          required_features=[Feature("JDK")],
                          implementation=DockerFile("server/Dockerfile")),
                Component("jdk",
                          provided_features=[Feature("JDK")],
                          implementation=DockerFile("jdk/Dockerfile")),
            ],
            Goals(services=[Service("Awesome")])
        )

        server_0 = Instance("server_0", model.resolve("server"))
        jdk_0 = Instance("jdk_0", model.resolve("jdk"))
        server_0.feature_provider = jdk_0

        configuration = Configuration( model, [ server_0,
                                                jdk_0 ])
        self.build(configuration)

        self.assert_generated(
            "config_0/images/server_0/Dockerfile",
            with_patterns=[
                "FROM camp-jdk_0"
            ])

        self.assert_generated(
            "config_0/images/jdk_0/Dockerfile",
            with_patterns=[
                "FROM openjdk:8-jre"
            ])




class NoDockerFileIsGenerated(BuilderTest):


    def test_when_a_component_is_implemented_by_a_docker_image(self):

        model = Model(
            [
                Component("server",
                          provided_services=[Service("Awesome")],
                          implementation=DockerImage("fchauvel/test:1.0.0"))
            ],
            Goals(services=[Service("Awesome")])
        )

        instance = Instance("server_0", model.resolve("server"))
        configuration = Configuration(model, [instance])

        self.build(configuration)

        self.assert_no_image_generated(0)
