#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Model, Component, Goals, Configuration, \
    Instance, Service, Feature, DockerImage, DockerFile
from camp.realize import Builder

from os import listdir, makedirs
from os.path import isdir, exists, join as join_paths

from shutil import rmtree

from unittest import TestCase



class BuilderTest(TestCase):


    def setUp(self):
        if isdir(self.WORKING_DIRECTORY):
            rmtree(self.WORKING_DIRECTORY)
        makedirs(self.WORKING_DIRECTORY)

        makedirs(join_paths(self.WORKING_DIRECTORY, "server"))
        path = join_paths(self.WORKING_DIRECTORY, "server", "Dockerfile")
        with open(path, "w") as docker_file:
            docker_file.write(self.DOCKER_FILE)

        makedirs(join_paths(self.WORKING_DIRECTORY, "jdk"))
        path = join_paths(self.WORKING_DIRECTORY, "jdk", "Dockerfile")
        with open(path, "w") as docker_file:
            docker_file.write(self.DOCKER_FILE)

        self._builder = Builder()

    WORKING_DIRECTORY = "temp/realize"

    DOCKER_FILE = ("FROM openjdk:8-jre\n"
                   "RUN echo this is nice\n")

    def build(self, configuration):
        self._builder.build(configuration, self.WORKING_DIRECTORY)


    def assert_directory_structure(self, expected_components):
        self.assertTrue(isdir(self.image_directory), "No image directory!")
        self.assertItemsEqual(expected_components,
                              self.generated_components())


    @property
    def image_directory(self):
        return join_paths(self.WORKING_DIRECTORY, "images")


    def generated_components(self):
        return [each_file \
                for each_file in listdir(self.image_directory)\
                if isdir(join_paths(self.image_directory, each_file)) ]


    def assert_docker_file_built_from(self, source_image, component):
        path = join_paths(self.image_directory, component, "Dockerfile")
        with open(path, "r") as docker_file:
            content = docker_file.read()
            self.assertIn("FROM " + source_image, content)



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

        self.assert_directory_structure(["server_0"])
        self.assert_docker_file_built_from("openjdk:8-jre", "server_0")


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

        self.assert_directory_structure(["server_0"])
        self.assert_docker_file_built_from("fchauvel/test:1.0.1", "server_0")


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

        self.assert_directory_structure(["server_0", "jdk_0"])
        self.assert_docker_file_built_from("camp-jdk_0", "server_0")
        self.assert_docker_file_built_from("openjdk:8-jre", "jdk_0")



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

        self.assert_directory_structure([])
