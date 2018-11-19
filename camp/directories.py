#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.graphviz import Graphviz

from os import makedirs, listdir
from os.path import isdir, join as join_paths, dirname

from re import search



class Directory(object):

    
    def __init__(self, path):
        self._path = path


    @property
    def path(self):
        return self._path

    


class InputDirectory(Directory):


    def __init__(self, path, codec):
        super(InputDirectory, self).__init__(path)
        self._codec = codec


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
        raise ValueError("Unable to find the CAMP model")

    MODEL_NAMES = [
        "model.yaml", "model.yml",
        "camp.yml", "camp.yaml",
        "input.yml", "input.yml"
    ]



class OutputDirectory(Directory):

    
    def __init__(self, path, codec):
        super(OutputDirectory, self).__init__(path)
        self._codec = codec


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
        for each_file in listdir(self._path):
            path = join_paths(self._path, each_file)
            if search(self.CONFIGURATION_FOLDER, path) \
               and isdir(path):
                yaml_file = join_paths(path, self.YAML_CONFIGURATION)
                with open(yaml_file, "r") as stream:
                    configuration = self._codec.load_configuration_from(model, stream)
                    yield path, configuration

    CONFIGURATION_FOLDER = r"config_[0-9]+$"

    
    def create_file(self, path, content):
        folder = dirname(path)
        self._create(folder)
        with open(path, "w") as stream:
            stream.write(content)
