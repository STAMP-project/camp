#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import DockerFile, DockerImage

from os import makedirs
from os.path import isdir, join as join_paths

from re import sub

from shutil import rmtree, copyfile



class Builder(object):


    def __init__(self):
        self._workspace = "/temp"


    def build(self, configuration, workspace=None):
        if workspace:
            self._workspace = workspace
        self._prepare_workspace()
        for each_instance in configuration.instances:
            self._copy_model_docker_file_for(each_instance)
            if each_instance.feature_provider:
                self._adjust_docker_file(each_instance)


    def _prepare_workspace(self):
        self._clean_or_create(self._image_directory)


    @staticmethod
    def _clean_or_create(directory):
        if isdir(directory):
            rmtree(directory)
        makedirs(directory)


    @property
    def _image_directory(self):
        return join_paths(self._workspace, "images")


    def _copy_model_docker_file_for(self, instance):
        if type(instance.definition.implementation) is DockerFile:
            self._clean_or_create(self._directory_for(instance))
            copyfile(self._model_docker_file(instance),
                     self._docker_file_for(instance))


    def _directory_for(self, instance):
        return join_paths(self._image_directory,
                          instance.name)


    def _model_docker_file(self, instance):
        return join_paths(self._workspace,
                          instance.definition.implementation.docker_file)

    def _docker_file_for(self, instance):
        return join_paths(self._directory_for(instance),"Dockerfile")


    def _adjust_docker_file(self, instance):
        host = instance.feature_provider.definition.implementation
        kind = type(host)
        if kind == DockerImage:
            self._replace_in_docker_file(
                instance,
                self.REGEX_FROM,
                "FROM " + host.docker_image)
        elif kind == DockerFile:
            self._replace_in_docker_file(
                instance,
                self.REGEX_FROM,
                "FROM camp-%s" % instance.feature_provider.name)
        else:
            raise RuntimeError("Component implement '%s' not supported yet" \
                               % kind.__name__)

    REGEX_FROM = r'FROM\s+([a-zA-Z0-9\._-]*/?[a-zA-Z0-9\._-]+:[a-zA-Z0-9\._-]+)'


    def _replace_in_docker_file(self, instance, pattern, replacement):
        path = self._docker_file_for(instance)
        with open(path, "r") as docker_file:
            content = docker_file.read()
        with open(path, "w") as docker_file:
            new_content = sub(pattern,
                              replacement,
                              content)
            docker_file.write(new_content)

