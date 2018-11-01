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
from os.path import exists, isdir, join as join_paths, split as split_path

from re import sub

from shutil import rmtree, copytree, copyfile



class Builder(object):


    def __init__(self):
        self._input_directory = "/temp"
        self._output_directory = "config"


    def build(self, configuration, input_directory=None, output_directory=None):
        if input_directory:
            self._input_directory = input_directory
        if output_directory:
            self._output_directory = output_directory

        self._prepare_output_directory()
        for each_instance in configuration.instances:
            self._copy_docker_compose_file()
            self._copy_template_for(each_instance)
            if each_instance.feature_provider:
                self._adjust_docker_file(each_instance)
            self._realize_variables(each_instance)


    def _prepare_output_directory(self):
        self._clean_or_create(self._image_directory)


    @staticmethod
    def _clean_or_create(directory):
        if isdir(directory):
            rmtree(directory)
        makedirs(directory)


    @property
    def _image_directory(self):
        return join_paths(self._output_directory, "images")


    def _copy_docker_compose_file(self):
        template = join_paths(self._input_directory, "docker-compose.yml")
        if exists(template):
            print " - Copying %s" % template
            copyfile(template,
                     join_paths(self._output_directory, "docker-compose.yml"))


    def _copy_template_for(self, instance):
        if isinstance(instance.definition.implementation, DockerFile):
            copytree(self._template_for(instance),
                     self._directory_for(instance))


    def _template_for(self, instance):
        return join_paths(self._input_directory, instance.definition.name)


    def _directory_for(self, instance):
        return join_paths(self._image_directory,
                          instance.name)


    def _docker_file_for(self, instance):
        return self._file_for(instance,
                              join_paths(instance.definition.name, "Dockerfile"))


    def _file_for(self, instance, resource):
        if instance.definition.name in resource:
            _, path = split_path(resource)
            return join_paths(self._directory_for(instance), path)
        else:
            return join_paths(self._output_directory, resource)

    def _adjust_docker_file(self, instance):
        host = instance.feature_provider.definition.implementation
        kind = type(host)
        if kind == DockerImage:
            self._replace_in(
                self._docker_file_for(instance),
                instance,
                self.REGEX_FROM,
                "FROM " + host.docker_image)
        elif kind == DockerFile:
            self._replace_in(
                self._docker_file_for(instance),
                instance,
                self.REGEX_FROM,
                "FROM camp-%s" % instance.feature_provider.name)
        else:
            raise RuntimeError("Component implement '%s' not supported yet" \
                               % kind.__name__)

    REGEX_FROM = r'FROM\s+([a-zA-Z0-9\._-]*/?[a-zA-Z0-9\._-]+:[a-zA-Z0-9\._-]+)'



    def _realize_variables(self, instance):
        for variable, value in instance.configuration:
            index = variable.domain.index(value)
            self._realize(instance, variable, index)


    def _realize(self, instance, variable, selected_index):
        for each_substitution in variable.realization:
            for each_target in each_substitution.targets:
                self._replace_in(
                    self._file_for(instance, each_target),
                    instance,
                    each_substitution.pattern,
                    each_substitution.replacements[selected_index])


    def _replace_in(self, path, instance, pattern, replacement):
        with open(path, "r") as resource_file:
            content = resource_file.read()
        with open(path, "w") as resource_file:
            new_content = sub(pattern,
                              replacement,
                              content)
            resource_file.write(new_content)
