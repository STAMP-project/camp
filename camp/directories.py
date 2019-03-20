#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.graphviz import Graphviz
from camp.codecs.yaml import YAML

from os import makedirs, listdir
from os.path import exists, isdir, join as join_paths, dirname

from re import search, sub



class NoConfigurationFound(Exception):


    def __init__(self, path):
        self._path = path


    @property
    def searched_folder(self):
        return self._path



class MissingModel(Exception):


    def __init__(self, directory, candidates):
        self._candidates = candidates
        self._folder = directory


    @property
    def searched_folder(self):
        return self._folder

    @property
    def searched_files(self):
        return self._candidates



class Directory(object):


    def __init__(self, path):
        self._path = path


    @property
    def path(self):
        return self._path



class InputDirectory(Directory):


    def __init__(self, path, codec=None):
        super(InputDirectory, self).__init__(path)
        self._codec = codec or YAML()


    @property
    def model(self):
        file_name = self._find_model()
        path = join_paths(self._path, file_name)
        with open(path, "r") as stream:
            model = self._codec.load_model_from(stream)
            return path, model, self._codec.warnings


    def _find_model(self):
        for any_file in listdir(self._path):
            for any_valid_name in self.MODEL_NAMES:
                if any_file == any_valid_name:
                    return any_file
        raise MissingModel(self._path, self.MODEL_NAMES)


    MODEL_NAMES = [
        "model.yaml", "model.yml",
        "camp.yml", "camp.yaml",
        "input.yml", "input.yml"
    ]


    def create_model(self, content):
        model = join_paths(self._path, self.MODEL_NAMES[2])
        with open(model, "w") as resource:
            resource.write(content)


    def create_template_file(self, component_name, path, content):
        resource = join_paths(self._path, self.TEMPLATE_FOLDER, component_name, path)
        folder = dirname(resource)
        if not isdir(folder):
            makedirs(folder)
        with open(resource, "w") as stream:
            stream.write(content)

    TEMPLATE_FOLDER = "template"


    @property
    def component_templates(self):
        templates = []
        for any_file in listdir(self.TEMPLATE_FOLDER):
            if isdir(any_file):
                templates.append(any_file)
        return templates



class OutputDirectory(Directory):


    def __init__(self, path, codec=None):
        super(OutputDirectory, self).__init__(path)
        self._codec = codec or YAML()


    def save_as_yaml(self, index, configuration):
        yaml_file = self._yaml_configuration_file(index)
        with open(yaml_file, "w") as stream:
            self._codec.save_configuration(configuration, stream)
        return yaml_file


    def _yaml_configuration_file(self, index):
        folder = self._folder_for_configuration(index)
        return join_paths(folder, self.YAML_CONFIGURATION)

    YAML_CONFIGURATION = "configuration.yml"


    def _folder_for_configuration(self, index):
        folder = join_paths(self._path, "config_%d" % index)
        self._create(folder)
        return folder


    @staticmethod
    def _create(directory):
        if not isdir(directory):
            makedirs(directory)


    def save_as_graphviz(self, index, configuration):
        graphviz_file = self._graphviz_configuration_file(index)
        with open(graphviz_file, "w") as stream:
            graphviz = Graphviz()
            graphviz.save_configuration(configuration, stream)
        return graphviz_file


    def _graphviz_configuration_file(self, index):
        folder = self._folder_for_configuration(index)
        return join_paths(folder, "configuration.dot")


    def existing_configurations(self, model):
        if not isdir(self._path):
            folder = sub(r"out[\\\/]?$","", self._path)
            raise NoConfigurationFound(folder)
        for each_file in listdir(self._path):
            path = join_paths(self._path, each_file)
            if search(self.CONFIGURATION_FOLDER, path) \
               and isdir(path):
                yaml_file = join_paths(path, self.YAML_CONFIGURATION)
                with open(yaml_file, "r") as stream:
                    configuration = self._codec.load_configuration_from(model, stream)
                    yield path, configuration

    CONFIGURATION_FOLDER = r"config_[0-9]+$"


    def images_generated_for(self, index):
        images = []
        folder = join_paths(self._path, "config_%d" % index, "images")
        for any_file in listdir(folder):
            if isdir(any_file):
                images.append(any_file)
        return images


    def create_file(self, path, content):
        folder = dirname(path)
        self._create(folder)
        with open(path, "w") as stream:
            stream.write(content)


    def has_file(self, path_to_file):
        resource = join_paths(self._path, path_to_file)
        return exists(resource)


    def content_of(self, path_to_file):
        resource = join_paths(self._path, path_to_file)
        with open(resource, "r") as stream:
            return stream.read()
