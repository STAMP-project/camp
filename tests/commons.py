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
from camp.directories import InputDirectory, OutputDirectory
from camp.generate import Z3Problem
from camp.realize import Builder

from os import makedirs, listdir
from os.path import exists, isdir, join as join_paths

from shutil import copytree, copy2

from tempfile import mkdtemp

from unittest import TestCase



SAMPLE_DIRECTORY = "samples"

class Scenario(object):


    @staticmethod
    def from_sample(relative_path):
        scenario = Scenario()
        sample_directory = join_paths(SAMPLE_DIRECTORY, relative_path)
        working_directory = scenario.directory

        # Copy all the content
        for item in listdir(sample_directory):
            source = join_paths(sample_directory, item)
            destination = join_paths(working_directory, item)
            if isdir(source):
                copytree(source, destination)
            else:
                copy2(source, destination)
        return scenario


    def __init__(self, path=""):
        temporary_directory = join_paths(mkdtemp(prefix="camp_"), path)
        makedirs(temporary_directory, exist_ok=True)
        self._input = InputDirectory(temporary_directory, YAML())
        self._output = OutputDirectory(join_paths(self._input.path, "out"), YAML())
        self._model = None


    @property
    def directory(self):
        return self._input.path


    @property
    def output_directory(self):
        return self._output.path


    @property
    def generated_configurations(self):
        _, model, warnings = self._input.model

        if warnings:
            error = ("There are warnings!\n"
                     "\n".join(each for each in warnings))
            raise AssertionError(error)

        return [GeneratedConfiguration(path, configuration) \
                for path, configuration in self._output.existing_configurations(model)]


    def fetch_test_report(self):
        return self._output.load_reports()


    @property
    def model(self):
        return self._input.model


    def create_configuration(self, index, content):
        file_name = self._output._yaml_configuration_file(index)
        self._output.create_file(file_name, content)


    def create_model(self, content):
        self._input.create_model(content)


    def create_template(self, component, relative_path, content="whatever"):
        self._input.create_template_file(component, relative_path, content)



class GeneratedConfiguration(object):


    def __init__(self, path, model):
        self._path = path
        self._model = model


    @property
    def model(self):
        return self._model


    def includes_file(self, path_to_file):
        return exists(join_paths(self._path, path_to_file))


    def content_of(self, resource):
        path = join_paths(self._path, resource)
        with open(path, "r") as content:
            return content.read()



class CampTest(TestCase):

    __test__ = False


    def generate_all(self):
        self.camp("generate", "--mode", "all", "-d", self.scenario.directory)


    def generate_coverage(self):
        self.camp("generate", "--mode", "covering", "-d", self.scenario.directory)


    def realize(self):
        self.camp("realize", "-d", self.scenario.directory)


    def execute(self, simulated=False, include=None):
        parameters = ["execute", "-d", self.scenario.directory]
        if simulated:
            parameters.append("-s")
        if include:
            parameters.append("--include")
            for each in include:
                parameters.append(str(each))
        self.camp(*parameters)

    @staticmethod
    def camp(*arguments):
        camp = Camp(YAML(), Z3Problem, Builder())
        command = Command.extract_from(arguments)
        command.send_to(camp)


    def _assert_generated(self, configuration, *files):
        for each in files:
            self.assertTrue(configuration.includes_file(each),
                            "Missing file '%s'" % each)

    def _assert_missing(self, configuration, *files):
        for each in files:
            self.assertFalse(configuration.includes_file(each),
                             "Unexpected file '%s'" % each)

    def assert_file_contains(self, configuration, resource, fragment):
        self.assertIn(fragment, configuration.content_of(resource))

    def create_configurations(self, *configurations):
        for index, configuration in enumerate(configurations, 1):
            self.scenario.create_configuration(index, configuration)
