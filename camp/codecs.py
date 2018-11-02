#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Model, Component, Service, Goals, Variable, \
    Feature, DockerFile, DockerImage, Substitution, Instance, Configuration

from yaml import load as load_yaml, dump as yaml_dump



class YAMLCodec(object):


    def __init__(self):
        self._warnings = []


    def save_configuration(self, configuration, stream):
        dictionary = self._as_dictionary(configuration)
        yaml_dump(dictionary, stream, default_flow_style=False)


    def _as_dictionary(self, configuration):
        dictionary = {}
        dictionary[Keys.INSTANCES] = []
        for each_instance in configuration.instances:
            instance = {}
            instance[Keys.NAME] = each_instance.name
            instance[Keys.DEFINITION] = each_instance.definition.name
            instance[Keys.FEATURE_PROVIDER] = each_instance.feature_provider.name
            instance[Keys.SERVICE_PROVIDERS] = [ each.name \
                                                 for each in each_instance.service_providers]
            instance[Keys.CONFIGURATION] = {}
            for variable, value in each_instance.configuration:
                instance[Keys.CONFIGURATION][variable.name] = value
                
            dictionary[Keys.INSTANCES].append(instance)
        return dictionary


    def load_configuration_from(self, model, stream):
        data = load_yaml(stream)
        
        instances = [ self._create_instance(model, item) \
                      for item in data[Keys.INSTANCES].values() ]

        result = Configuration(model, instances)

        for each in instances:
            self._connect_instance(result, each, data[Keys.INSTANCES][each.name])

        return result

    
    @staticmethod
    def _create_instance(model, data):
        name = data[Keys.NAME]
        definition = model.resolve(data[Keys.DEFINITION])
        configuration = []
        if Keys.CONFIGURATION in data:
            for variable_name, value in data[Keys.CONFIGURATION].items():
                for any_variable in definition.variables:
                    if any_variable.name == variable_name:
                        configuration.append((any_variable, value))
                        break
                else:
                    raise RuntimeError("Variable '%s' has no match in the model" % variable_name)
        return Instance(name, definition, configuration)


    @staticmethod
    def _connect_instance(configuration, instance, data):
        if Keys.FEATURE_PROVIDER in data \
           and data[Keys.FEATURE_PROVIDER]:
            provider = configuration.resolve(data[Keys.FEATURE_PROVIDER])
            instance.feature_provider = provider
        if Keys.SERVICE_PROVIDERS in data:
            providers = [configuration.resolve(each_provider) \
                         for each_provider in data[Keys.SERVICE_PROVIDERS]]
            instance.service_providers = providers


    def load_model_from(self, stream):
        data = load_yaml(stream)
        components = []
        goals = Goals()
        for key, item in data.items():
            if key == Keys.COMPONENTS:
                if type(item) != dict:
                    self._wrong_type(dict, type(item), key)
                    continue
                components = self._parse_components(item)
            elif key == Keys.GOALS:
                if type(item) != dict:
                    self._wrong_type(dict, type(item), key)
                    continue
                goals = self._parse_goals(item)
            else:
                self._ignore(key)
        return Model(components, goals)


    def _parse_components(self, data):
        components = []
        for key, item in data.items():
            components.append(self._parse_component(key, item))
        return components


    def _parse_component(self, name, data):
        provided_services = []
        required_services = []
        provided_features = []
        required_features = []
        variables = []
        implementation = None

        for key, item in data.items():

            if key == Keys.PROVIDES_SERVICES:
                if type(item) != list:
                    self._wrong_type(list, type(item), Keys.COMPONENTS, name, key)
                    continue
                for each_name in item:
                    provided_services.append(Service(self._escape(each_name)))

            elif key == Keys.REQUIRES_SERVICES:
                if type(item) != list:
                    self._wrong_type(list, type(item), Keys.COMPONENTS, name, key)
                    continue
                for each_name in item:
                    required_services.append(Service(self._escape(each_name)))

            elif key == Keys.PROVIDES_FEATURES:
                if type(item) != list:
                    self._wrong_type(list, type(item), Keys.COMPONENTS, name, key)
                    continue
                for each_name in item:
                    provided_features.append(Feature(self._escape(each_name)))

            elif key == Keys.REQUIRES_FEATURES:
                if type(item) != list:
                    self._wrong_type(list, type(item), Keys.COMPONENTS, name, key)
                    continue
                for each_name in item:
                    required_features.append(Feature(self._escape(each_name)))

            elif key == Keys.VARIABLES:
                if type(item) != dict:
                    self._wrong_type(dict, type(item), Keys.COMPONENTS, name, key)
                    continue
                variables = self._parse_variables(name, item)

            elif key == Keys.IMPLEMENTATION:
                if type(item) != dict:
                    self._wrong_type(dict, type(item), Keys.COMPONENTS, name, key)
                    continue
                implementation = self._parse_implementation(name, item)
                
            else:
                self._ignore(Keys.COMPONENTS, name, key)


        return Component(name,
                         provided_services=provided_services,
                         required_services=required_services,
                         provided_features=provided_features,
                         required_features=required_features,
                         variables=variables,
                         implementation=implementation)

    def _escape(self, name):
        if type(name) is not str:
            return "_" + str(name)
        return name

    def _parse_variables(self, component, data):
        variables = []
        for key, item in data.items():
            variables.append(self._parse_variable(component, key, item))
        return variables


    def _parse_variable(self, component, name, data):
        domain = []
        realization = []
        for key, item in data.items():
            if key == Keys.DOMAIN:
                for each_value in data[key]:
                    domain.append(str(each_value))
            elif key == Keys.REALIZATION:
                for index, each in enumerate(data[key], 1):
                    substitution = self._parse_substitution(component, name, index, each)
                    realization.append(substitution)
            else:
                self._ignore(Keys.COMPONENTS, component, Keys.VARIABLES, name, key)
                
        return Variable(name, domain, realization)


    def _parse_substitution(self, component, variable, index, data):
        path = [Keys.COMPONENTS,
                component,
                Keys.VARIABLES,
                variable,
                Keys.REALIZATION,
                "#%d" % index]
                             
        targets = []
        pattern = self.UNDEFINED_PATTERN
        replacements = []
        for key, item in data.items():

            if key == Keys.TARGETS:
                if type(data[key]) is not list:
                    self._wrong_type(list, type(data[key]), *(path + [key]))
                    continue
                targets = [each for each in data[key]]

            elif key == Keys.PATTERN:
                pattern = data[key]

            elif key == Keys.REPLACEMENTS:
                if type(data[key]) is not list:
                    self._wrong_type(list, type(data[key]), *(path + [key]))
                    continue
                replacements = [each for each in data[key]]

            else:
                self._ignore(*(path + [key]))
        
        if not targets:
            self._missing([Keys.TARGETS], *path)

        if pattern == self.UNDEFINED_PATTERN:
            self._missing([Keys.PATTERN], *path)

        if not replacements:
            self._missing([Keys.REPLACEMENTS], *path)
            
        return Substitution(targets, pattern, replacements)

    UNDEFINED_PATTERN = "missing pattern!"
    

    def _parse_implementation(self, name, data):
        implementation = None
        for key, item in data.items():
            if key == Keys.DOCKER:
                implementation = self._parse_docker(name, item)
            else:
                self._ignore(Keys.COMPONENTS, name, Keys.IMPLEMENTATION, key)
        return implementation


    def _parse_docker(self, name, data):
        docker = None
        for key, item in data.items():
            if key == Keys.FILE:
                docker = DockerFile(self._escape(item))
            elif key == Keys.IMAGE:
                docker = DockerImage(self._escape(item))
            else:
                self._ignore(Keys.COMPONENTS, name, Keys.IMPLEMENTATION, Keys.DOCKER, key)

        if not docker:
            self._missing(
                [Keys.FILE, Keys.IMAGE],
                Keys.COMPONENTS, name, Keys.IMPLEMENTATION, Keys.DOCKER)
            
        return docker


    def _parse_goals(self, data):
        running_services = []
        for key, item in data.items():
            if key == Keys.RUNNING:
                if type(item) != list:
                    self._wrong_type(list, type(item), Keys.GOALS, key)
                    continue
                for index, each_name in enumerate(item, 1):
                    running_services.append(Service(str(each_name)))
            else:
                self._ignore(Keys.GOALS, key)
                
        return Goals(running_services)


    def _ignore(self, *path):
        self._warnings.append(IgnoredEntry(*path))


    def _wrong_type(self, expected, found, *path):
        self._warnings.append(WrongType(expected, found, *path))

        
    def _missing(self, *path):
        self._warnings.append(MissingEntry(*path))
        

    @property
    def warnings(self):
        return self._warnings



class Keys:
    """
    The labels that are fixed in the YAML
    """
    
    COMPONENTS = "components"
    CONFIGURATION = "configuration"
    DEFINITION = "definition"
    DOCKER = "docker"
    DOMAIN = "domain"
    FEATURE_PROVIDER = "feature_provider"
    FILE = "file"
    GOALS = "goals"
    IMAGE = "image"
    IMPLEMENTATION = "implementation"
    INSTANCES = "instances"
    NAME = "name"
    PATTERN = "pattern"
    PROVIDES_FEATURES = "provides_features"
    PROVIDES_SERVICES = "provides_services"
    REALIZATION = "realization"
    REPLACEMENTS = "replacements"
    REQUIRES_FEATURES = "requires_features"
    REQUIRES_SERVICES = "requires_services"
    RUNNING = "running"
    SERVICE_PROVIDERS = "service_providers"
    TARGETS = "targets"
    VARIABLES = "variables"



class Warning(object):

    def __init__(self, *path):
        self._path = "/".join(path)


    @property
    def path(self):
        return self._path
    


class IgnoredEntry(Warning):

    def __init__(self, *path):
        super(IgnoredEntry, self).__init__(*path)

    def __str__(self):
        return "Entry '%s' ignored!" % self._path


    
class WrongType(Warning):

    def __init__(self, expected, found, *path):
        super(WrongType, self).__init__(*path)
        self._expected = expected.__name__
        self._found = found.__name__

    @property
    def found(self):
        return self._found


    @property
    def expected(self):
        return self._expected


    def __str__(self):
        return "Wrong type at '%s'! Expected '%s' but found '%s'." % (self._path,
                                                                  self._expected,
                                                                  self._found)

class MissingEntry(Warning):


    def __init__(self, candidates, *path):
        super(MissingEntry, self).__init__(*path)
        self._candidates = candidates


    def __str__(self):
        return "Incomplete entry '%s'! Possibly missing entries %s" \
            % (self._path,
               ", ".join("'%s'" % each for each in self._candidates))

    @property
    def candidates(self):
        return [each for each in self._candidates]
