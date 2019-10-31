#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import DockerFile, DockerImage, Substitution, \
    ResourceSelection, ComponentResourceSelection

from os import listdir, makedirs, remove, sep as path_separator
from os.path import exists, isdir, isfile, join as join_paths, \
     normpath, split as split_path, relpath

from pkgutil import get_data

from re import escape, sub, subn

from shutil import copyfile, copytree, move, rmtree




class InvalidSubstitution(Exception):
    """
    Thrown when no match is found when performing a substitution
    """

    def __init__(self, target, pattern, content):
        self._target = target
        self._pattern = pattern
        self._content = content

    @property
    def target(self):
        return self._target


    @property
    def pattern(self):
        return self._pattern


    @property
    def content(self):
        return self._content



class Builder(object):


    def __init__(self):
        self._input_directory = "/temp"
        self._output_directory = "config"
        self._images = []


    def build(self, configuration, input_directory=None, output_directory=None):
        """
        Entry point of the realization engine
        """
        self._images = []
        if input_directory:
            self._input_directory = input_directory
        if output_directory:
            self._output_directory = output_directory

        self._prepare_output_directory()
        self._copy_orchestration_files()
        for each_instance in configuration.instances:
            self._copy_template_for(each_instance)
            self._adjust_docker_file(each_instance)
            self._realize_component(each_instance)
            self._realize_variables(each_instance)
        self._adjust_docker_compose_file(configuration)
        self._generate_build_script()


    def _prepare_output_directory(self):
        self._clean_or_create(self._image_directory)


    def _copy_orchestration_files(self):
        count = 0
        for any_file in listdir(self._template_folder):
            path_to_file = join_paths(self._template_folder, any_file)
            if isfile(path_to_file):
                count += 1
                destination = join_paths(self._output_directory, any_file)
                copyfile(path_to_file, destination)

    @staticmethod
    def _clean_or_create(directory):
        if isdir(directory):
            rmtree(directory)
        makedirs(directory)


    @property
    def _image_directory(self):
        return join_paths(self._output_directory, "images")


    def _adjust_docker_compose_file(self, configuration):
        orchestration = join_paths(self._output_directory, "docker-compose.yml")
        if exists(orchestration):
            with open(orchestration, "r") as source:
                content = source.read()
                for each_instance in configuration.instances:
                    # Issue 82: Here we replace "build" clauses by
                    # "images" clauses to avoid generating additional
                    # dangling images
                    content, count = subn(r"build:\s*\./" + each_instance.definition.name,
                                          "image: " + self._docker_tag_for(each_instance),
                                          content)

            with open(orchestration, "w") as target:
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
        normalized_path = normpath(resource)
        parts = normalized_path.split(path_separator)
        if instance.definition.name in parts:
            path = relpath(resource, instance.definition.name)
            return join_paths(self._directory_for(instance), path)
        else:
            return join_paths(self._output_directory, resource)


    def _adjust_docker_file(self, instance):
        self._record_dependency_of(instance)
        if not instance.feature_provider:
            pass
            # Nothing to change on the dockerfile
        else:
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

    # Issue 78 about Multi-stages build.
    # We do not match every single FROM statement, but only those that
    # start with 'camp', such as 'camp/runtime' for instance.
    REGEX_FROM = r'FROM\s+camp/[a-zA-Z0-9\._-]+(?:\:[a-zA-Z0-9\._-]+)?'


    def _realize_component(self, instance):
        for any_action in instance.definition.realization:
            if isinstance(any_action, ComponentResourceSelection):
                self._rename(instance,
                             any_action.selected_resource,
                             any_action.alias)
                for each_alternative in any_action.alternatives:
                    self._delete(instance, each_alternative)

            else:
                message = UNSUPPORTED_COMPONENT_REALIZATION.format(type(any_action))
                raise RuntimeError(message)

    UNSUPPORTED_COMPONENT_REALIZATION = \
        "Unsupported component realization action: '{}'"


    def _realize_variables(self, instance):
        for variable, value in instance.configuration:
            self._realize(instance, variable, value)


    def _realize(self, instance, variable, value):
        for each_realization in variable.realization:
            if isinstance(each_realization, Substitution):
                self._substitute(instance, variable, value, each_realization)

            elif isinstance(each_realization, ResourceSelection):
                self._select_resource(instance, variable, value, each_realization)

            else:
                message = self.UNKNOWN_REALIZATION_TYPE.format(
                    type=type(each_realization))
                raise ValueError(message)

    UNKNOWN_REALIZATION_TYPE = "Realization type '{type}' is not yet supported!"


    def _substitute(self, instance, variable, value, substitution):
        for each_target in substitution.targets:
            replacement = self._select_replacement(variable, substitution, value)
            self._replace_in(
                self._file_for(instance, each_target),
                instance,
                substitution.pattern,
                replacement,
                escape_pattern=True)


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


    def _replace_in(self, path, instance, pattern, replacement, escape_pattern=False):
        with open(path, "r+") as resource_file:
            content = resource_file.read()

            escaped_pattern = pattern
            if escape_pattern:
                escaped_pattern = escape(pattern)
            new_content, match_count = subn(escaped_pattern,
                                            replacement,
                                            content)
            if match_count == 0:
                raise InvalidSubstitution(path, pattern, content)

            resource_file.seek(0)
            resource_file.write(new_content)
            resource_file.truncate()


    def _select_resource(self, instance, variable, value, selection):
        deletions = 0
        for index, any_value in enumerate(variable.domain):
            if value == any_value:
                if selection.destination:
                    self._rename(instance,
                                 selection.resources[index],
                                 selection.destination)

            else:
                deletions += 1
                self._delete(instance, selection.resources[index])

        if deletions == len(variable.domain):
            raise RuntimeError("Everything deleted! {}/{} (value={})".format(
                instance.name, variable.name, value
            ))


    def _rename(self, instance, source, destination):
        resource = self._file_for(instance, source)
        renamed = self._file_for(instance, destination)
        move(resource, renamed)


    def _delete(self, instance, discarded):
        resource = self._file_for(instance, discarded)
        if isfile(resource):
            remove(resource)
        else:
            rmtree(resource)


    @staticmethod
    def _docker_tag_for(instance):
        return "camp-%s" % instance.name


    def _record_dependency_of(self, instance):
        if instance not in self._images:
            if instance.feature_provider:
                if instance.feature_provider in self._images:
                    index = self._images.index(instance.feature_provider)
                    self._images.insert(index+1, instance)
                else:
                    self._images.append(instance.feature_provider)
                    self._images.append(instance)
            else:
                self._images.insert(0, instance)
        else:
            if instance.feature_provider:
                if instance.feature_provider not in self._images:
                    index = self._images.index(instance)
                    self._images.insert(index, instance.feature_provider)


    def _generate_build_script(self):
        build_commands = []
        delete_commands = []
        for each_instance in self._images:
            if isinstance(each_instance.definition.implementation, DockerFile):
                tag = self._docker_tag_for(each_instance)
                delete_command = self.DELETE_COMMAND.format(image=tag)
                delete_commands.append(delete_command)
                folder = "./" + each_instance.name
                build_command = self.BUILD_COMMAND.format(folder=folder, tag=tag)
                build_commands.append(build_command)

        script = self._build_script()
        with open(script, "w") as stream:
            body = self._fetch_script_template()
            body = sub(self.BUILD_COMMAND_MARKER,
                       "\n    ".join(build_commands),
                       body)
            body = sub(self.OBSELETE_IMAGES_MARKER,
                       "\n    ".join(delete_commands),
                       body)
            stream.write(body)

    BUILD_COMMAND_MARKER = "{build_commands}"

    OBSELETE_IMAGES_MARKER = "{obselete_images}"

    def _fetch_script_template(self):
        return get_data('camp', 'data/manage_images.sh').decode("utf-8")


    # Issue 82: The "--force-rm" option avoids generating many
    # intermediate containers and consuming disk space
    BUILD_COMMAND = "docker build --force-rm --no-cache -t {tag} {folder}"

    DELETE_COMMAND = ("if [ -z \"$(docker images -q {image})\" ]; "
                     "then printf \"No such image {image}!\\\\n\"; "
                     "else docker rmi {image}; fi")

    def _build_script(self):
        return join_paths(self._image_directory, "build_images.sh")
