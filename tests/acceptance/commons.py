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

from os import makedirs
from os.path import exists, isdir, join as join_paths, basename

from shutil import copytree, rmtree

from tempfile import gettempdir


from unittest import TestCase



class Sample(object):


    def __init__(self, path, workspace=None):
        workspace = workspace or join_paths(gettempdir(), "acceptance")
        self._source = join_paths("samples", path)
        self._input = InputDirectory(self._copy(self._source, workspace), YAML())
        self._output = OutputDirectory(join_paths(self._input.path, "out"), YAML())
        self._model = None


    @staticmethod
    def _copy(source, workspace):
        destination = join_paths(workspace, basename(source))
        if source and exists(source):
            if isdir(destination):
                rmtree(destination)
            copytree(source, destination)

        else:
            if isdir(destination):
                rmtree(destination)
            makedirs(destination)
        return destination



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


    def create_template(self, component, relative_path, content):
        self._input.create_template_file(component, relative_path, content)




class GeneratedConfiguration(object):


    def __init__(self, path, model):
        self._path = path
        self._model = model


    def includes_file(self, path_to_file):
        return exists(join_paths(self._path, path_to_file))




class CampTests(TestCase):

    __test__ = False


    def generate_all(self):
        self.camp("generate", "--all", "-d", self.sample.directory)


    def generate_coverage(self):
        self.camp("generate", "--coverage", "-d", self.sample.directory)


    def realize(self):
        self.camp("realize", "-d", self.sample.directory)


    def execute(self, component, testing_tool):
        self.camp("execute",
                  "-d", self.sample.directory,
                  "-c", component,
                  "-t", testing_tool)


    @staticmethod
    def camp(*arguments):
        camp = Camp(YAML(), Z3Problem, Builder())
        command = Command.extract_from(arguments)
        command.send_to(camp)


    def _assert_generated(self, configuration, *files):
        for each in files:
            self.assertTrue(configuration.includes_file(each),
                            "Missing file '%s'" % each)


    def create_configurations(self, *configurations):
        for index, configuration in enumerate(configurations, 1):
            self.sample.create_configuration(index, configuration)
