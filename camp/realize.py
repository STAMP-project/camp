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
        self._images = []


    def build(self, configuration, input_directory=None, output_directory=None):
        self._images = []
        if input_directory:
            self._input_directory = input_directory
        if output_directory:
            self._output_directory = output_directory

        self._prepare_output_directory()
        self._generate_docker_compose_file(configuration)
        for each_instance in configuration.instances:
            self._copy_template_for(each_instance)
            if each_instance.feature_provider:
                self._adjust_docker_file(each_instance)
            self._realize_variables(each_instance)
        self._generate_build_script()


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


    def _generate_docker_compose_file(self, configuration):
        template = join_paths(self._template_folder, "docker-compose.yml")
        if exists(template):
            with open(template, "r") as source:
                content = source.read()
                for each_instance in configuration.instances:
                    content = sub(r"build:\s*\./" + each_instance.definition.name,
                                  "build: ./images/" + each_instance.name,
                                  content)

            destination = join_paths(self._output_directory, "docker-compose.yml")
            with open(destination, "w") as target:
                target.write(content)
                    

    def _copy_template_for(self, instance):
        if isinstance(instance.definition.implementation, DockerFile):
            copytree(self._template_for(instance),
                     self._directory_for(instance))


    def _template_for(self, instance):
        return join_paths(self._template_folder,
                          instance.definition.name)


    @property
    def _template_folder(self):
        return join_paths(self._input_directory,
                          self.TEMPLATE_FOLDER)
        
    TEMPLATE_FOLDER = "template"


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
        self._record_dependency_of(instance)
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
                "FROM %s" % self._docker_tag_for(instance.feature_provider))
        else:
            raise RuntimeError("Component implement '%s' not supported yet" \
                               % kind.__name__)

    REGEX_FROM = r'FROM\s+([a-zA-Z0-9\._-]*/?[a-zA-Z0-9\._-]+:[a-zA-Z0-9\._-]+)'



    def _realize_variables(self, instance):
        for variable, value in instance.configuration:
            self._realize(instance, variable, value)


    def _realize(self, instance, variable, value):
        for each_substitution in variable.realization:
            for each_target in each_substitution.targets:
                replacement = self._select_replacement(variable, each_substitution, value)
                self._replace_in(
                    self._file_for(instance, each_target),
                    instance,
                    each_substitution.pattern,
                    replacement)

    @staticmethod
    def _select_replacement(variable, substitution, value):
        if value in variable.domain \
           and len(substitution.replacements) == len(variable.domain):
            index = variable.domain.index(value)
            return substitution.replacements[index]
        if len(substitution.replacements) == 1 \
           and "{value}" in substitution.replacements[0]:
            return str(substitution.replacements[0]).format(value=value)
        raise RuntimeError("Invalid replacements for variable '%s'!" % variable.name)
                      

    def _replace_in(self, path, instance, pattern, replacement):
        with open(path, "r") as resource_file:
            content = resource_file.read()
        with open(path, "w") as resource_file:
            new_content = sub(pattern,
                              replacement,
                              content)
            resource_file.write(new_content)


    @staticmethod
    def _docker_tag_for(instance):
        return "camp-%s" % instance.name


    def _record_dependency_of(self, instance):
        if instance.feature_provider in self._images:
            index = self._images.index(instance.feature_provider)
            self._images.insert(index+1, instance)
        else:
            self._images.append(instance.feature_provider)
            self._images.append(instance)
            
        
                    
    def _generate_build_script(self):
        build_commands = []
        for each_instance in self._images:
            if isinstance(each_instance.definition.implementation, DockerFile):
                tag = self._docker_tag_for(each_instance)
                folder = "./" + each_instance.name
                command = self.BUILD_COMMAND.format(folder=folder, tag=tag)
                build_commands.append(command)

        build_script = self._build_script()
        with open(build_script, "w") as stream:
            content = self.BUILD_SCRIPT_TEXT.format("\n".join(build_commands))
            stream.write(content)
        
                                   
    BUILD_COMMAND = "docker build -t {tag} {folder}"

    def _build_script(self):
        return join_paths(self._image_directory, "build_images.sh")
        
    
    BUILD_SCRIPT_TEXT = ("#!/bin/bash\n"
                         "#\n"
                         "# Generated by CAMP. Edit carefully\n"
                         "#\n"
                         "# Build all images and set the appropriate tags\n"
                         "#\n"
                         "{0}\n"
                         "echo 'All images ready.'\n")
