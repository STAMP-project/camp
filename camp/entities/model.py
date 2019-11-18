#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from __future__ import unicode_literals

from future.utils import string_types as str



class Visitee(object):


    def accept(self, visitor, *context):
        """
        Dynamic visitor pattern. We compute the name of the "visit_X"
        method based on the name of class.
        """
        method_name = "visit_" + type(self).__name__.lower()
        method = getattr(visitor, method_name)
        if not callable(method):
            message = "Invalid visitor '%s'! Cannot handle object of type '%s'!"
            raise RuntimeError(message % (type(visitor).__name__,
                                          type(self).__name))
        method(self, *context)



class NamedElement(Visitee):
    """
    Abstract the name that all entities have.
    """

    def __init__(self, name):
        if not isinstance(name, str):
            raise AssertionError("name must be a string!")
        self._name = name


    @property
    def name(self):
        return self._name



class Model(Visitee):

    def __init__(self, components, goals, constraints=None):
        self._components = {each.name: each for each in components}
        self._goals = goals
        self._constraints = constraints or []


    def resolve(self, identifier):
        if identifier in self._components:
            return self._components[identifier]

        for any_service in self.services:
            if any_service.name == identifier:
                return any_service

        for any_feature in self.features:
            if any_feature.name == identifier:
                return any_feature

        raise KeyError(identifier)


    def __contains__(self, item):
        if isinstance(item, Feature):
            return item in self.features
        elif isinstance(item, Component):
            return item.name in self._components
        elif isinstance(item, Service):
            return item in self.services
        else:
            return None


    @property
    def tests(self):
        for any_component in self._components.values():
            if any_component.contains_tests:
                return any_component


    @property
    def services(self):
        services = []
        for each_component in self._components.values():
            services.extend(each_component.provided_services)
            services.extend(each_component.required_services)
        services.extend(self._goals.services)
        return list(set(services))


    @property
    def features(self):
        features = []
        for each_component in self._components.values():
            features.extend(each_component.provided_features)
            features.extend(each_component.required_features)
        features.extend(self._goals.features)
        return list(set(features))


    def component_named(self, name):
        return self._components.get(name, None)


    @property
    def components(self):
        return [each for each in self._components.values()]


    @property
    def goals(self):
        return self._goals


    @property
    def constraints(self):
        return self._constraints



class Service(NamedElement):
    """
    Immutable value object.
    """

    def __init__(self, name):
        super(Service, self).__init__(name)


    def __eq__(self, other):
        if not isinstance(other, Service):
            return False
        return self._name == other.name


    def __repr__(self):
        return "Service('%s')" % self._name


    def __hash__(self):
        return hash(self._name)



class Feature(NamedElement):
    """
    Immutable value object.
    """


    def __init__(self, name):
        super(Feature, self).__init__(name)


    def __eq__(self, other):
        if not isinstance(other, Feature):
            return False
        return self._name == other.name


    def __repr__(self):
        return "Feature('%s')" % self._name


    def __hash__(self):
        return hash(self._name)



class Component(NamedElement):


    def __init__(self, name,
                 provided_features=None,
                 required_features=None,
                 provided_services=None,
                 required_services=None,
                 variables=None,
                 implementation=None,
                 test_settings=None,
                 realization=None):
        super(Component, self).__init__(name)
        self._required_features = [each for each in required_features] \
                                  if required_features else []
        self._provided_features = [each for each in provided_features] \
                                  if provided_features else []
        self._required_services = [each for each in required_services] \
                                  if required_services else []
        self._provided_services = [each for each in provided_services] \
                                  if provided_services else []
        self._variables = {each.name: each for each in variables} \
                          if variables else {}
        self._implementation = implementation
        self._test_settings = test_settings
        self._realization = [each for each in realization] \
                            if realization else []


    @property
    def required_features(self):
        return [each for each in self._required_features]


    @property
    def provided_features(self):
        return [each for each in self._provided_features]


    @property
    def required_services(self):
        return [each for each in self._required_services]


    @property
    def provided_services(self):
        return [each for each in self._provided_services]


    @property
    def variables(self):
        return [each for each in self._variables.values()]


    @property
    def implementation(self):
        return self._implementation


    @property
    def contains_tests(self):
        return self._test_settings is not None


    @property
    def test_settings(self):
        return self._test_settings


    @property
    def realization(self):
        return self._realization



class Variable(NamedElement):


    @staticmethod
    def cover(minimum, maximum, coverage):

        def largest_smaller_divisor():
            return next(d for d in range(coverage, 0, -1) if width % d == 0)

        width = maximum - minimum

        divisor = largest_smaller_divisor()
        return [minimum + i * divisor \
                for i in range(int(width / divisor) + 1)]


    def __init__(self, name, value_type, values, realization=None):
        super(Variable, self).__init__(name)
        self._value_type = value_type
        self._values = [each for each in values]
        self._realization = [each for each in realization] \
                            if realization else []

    @property
    def value_type(self):
        return self._value_type


    @property
    def domain(self):
        return [each for each in self._values]


    @property
    def realization(self):
        return [each for each in self._realization]


    def value_at(self, index):
        if self._value_type != "Integer" and len(self._values) > 0:
            return self._values[index]
        else:
            return index



class Substitution(Visitee):
    """
    Value object
    """


    def __init__(self, targets, pattern, replacements):
        if not all(isinstance(t, str) for t in targets):
            raise AssertionError("Targets must be string objects!")
        self._targets = targets

        if not isinstance(pattern, str):
            raise AssertionError("Pattern must be a string object")
        self._pattern = pattern

        if not all(isinstance(r, str) for r in replacements):
            raise AssertionError("Replacements must be string objects!")
        self._replacements = replacements


    @property
    def targets(self):
        return [each for each in self._targets]


    @property
    def pattern(self):
        return self._pattern


    @property
    def replacements(self):
        return [each for each in self._replacements]


    def __eq__(self, other):
        if not isinstance(other, Substitution):
            return False
        return set(self._targets) == set(other.targets) \
            and self._pattern == other.pattern \
            and self._replacements == other.replacements


    def __hash__(self):
        return hash(
            tuple(
                sorted(self._targets) \
                + [self._pattern] \
                + self._replacements))



class ResourceSelection(Visitee):
    """
    Select a specific ressource, that is a file or a directory and the
    name it should take in the configuration.  Immutable value
    object
    """


    def __init__(self, destination, resources):
        self._destination = destination
        self._resources = [ each for each in resources ] if resources else []


    @property
    def destination(self):
        return self._destination


    @property
    def resources(self):
        return self._resources


    def __eq__(self, other):
        if not isinstance(other, ResourceSelection):
            return False
        return tuple([self._destination] + self._resources) \
            == tuple([other.destination] + other.resources)


    def __hash__(self):
        return hash(tuple([self._destination, *self._resources]))


    def __repr__(self):
        return "ResourceSelection(%s)" % self._resources



class Implementation(Visitee):
    pass



class DockerFile(Implementation):

    """
    Value objects
    """

    def __init__(self, file_path):
        if not isinstance(file_path, str):
            raise AssertionError(self.WRONG_TYPE % type(file_path))
        self._docker_file = file_path

    WRONG_TYPE = "Docker file must be a string (found '%s')."


    @property
    def docker_file(self):
        return self._docker_file


    def __eq__(self, other):
        if not isinstance(other, DockerFile):
            return False
        return self._docker_file == other.docker_file


    def __hash__(self):
        return hash(self._docker_file)


    def __repr__(self):
        return "DockerFile('%s')" % self._docker_file



class DockerImage(Implementation):
    """
    Value objects
    """

    def __init__(self, image):
        if not isinstance(image, str):
            raise AssertionError(self.WRONG_TYPE % type(image))
        self._docker_image = image

    WRONG_TYPE = "Docker image must be a string (found '%s')."


    @property
    def docker_image(self):
        return self._docker_image


    def __eq__(self, other):
        if not isinstance(other, DockerImage):
            return False
        return self._docker_image == other.docker_image


    def __hash__(self):
        return hash(self._docker_image)


    def __repr__(self):
        return "DockerImage('%s')" % self._docker_image



class ComponentResourceSelection(object):
    """
    Resource selection associated with a given component (as opposed to
    realisation actions associated with variables.

    Value object / data type
    """

    def __init__(self, selected_resource, alternatives, alias=None):
        if selected_resource in alternatives:
            message = self.INCONSISTENT_ALTERNATIVES.format(selected_resource,
                                                            alternatives)
            raise ValueError(message)
        self._selected = selected_resource
        self._alternatives = set(alternatives)
        self._alias = alias

    INCONSISTENT_ALTERNATIVES = ("The selected resource '{}' appears among "
                                 "alternatives '{}'")


    @property
    def selected_resource(self):
        return self._selected


    @property
    def alternatives(self):
        return self._alternatives


    @property
    def alias(self):
        return self._alias if self._alias else self._selected


    def __eq__(self, other):
        if not isinstance(other, ComponentResourceSelection):
            return False

        return self._selected == other._selected \
            and self._alternatives == other._alternatives \
            and self._alias == other._alias


    def __hash__(self):
        content = tuple([self._selected, self._alias]) \
                  + tuple(self._alternatives)
        return hash(content)


    def __repr__(self):
        return "ComponentResourceSelection('{}', {}, '{}')".format(
            self._selected,
            "[" + ",".join(self._alternatives) + "]",
            self._alias)


class TestSettings(object):
    """
    Immutable Value Object
    """


    def __init__(self, command, report_format, report_location, report_pattern, liveness_test=None):
        self._command = command
        self._report_format = report_format
        self._report_location = report_location
        self._report_pattern = report_pattern
        self._liveness_test = liveness_test


    @property
    def test_command(self):
        return self._command


    @property
    def report_format(self):
        return self._report_format


    @property
    def report_location(self):
        return self._report_location


    @property
    def report_pattern(self):
        return self._report_pattern


    @property
    def include_liveness_test(self):
        return self._liveness_test is not None

    @property
    def liveness_test(self):
        if not self.include_liveness_test:
            raise ValueError("There is no liveness test defined!")
        return self._liveness_test


    def __eq__(self, other):
        if not isinstance(other, TestSettings):
            return False

        return self._command == other.test_command \
            and self._report_format == other.report_format \
            and self._report_location == other.report_location \
            and self._report_pattern == other.report_pattern \
            and self._liveness_test == other._liveness_test

    def __hash__(self):
        return hash((self._command,
                     self._report_format,
                     self._report_location,
                     self._report_pattern,
                     self._liveness_test))



class Instance(NamedElement):

    def __init__(self, name, definition, configuration=None):
        super(Instance, self).__init__(name)
        self._definition = definition
        self._feature_provider = None
        self._service_providers = []
        self._configuration = configuration if configuration else []

    @property
    def definition(self):
        return self._definition


    @property
    def service_providers(self):
        return self._service_providers


    @service_providers.setter
    def service_providers(self, new_providers):
        self._service_providers = new_providers


    @property
    def feature_provider(self):
        return self._feature_provider


    @feature_provider.setter
    def feature_provider(self, new_provider):
        self._feature_provider = new_provider


    @property
    def configuration(self):
        return self._configuration


    @configuration.setter
    def configuration(self, new_configuration):
        self._configuration = new_configuration


    def __getitem__(self, key):
        for variable, value in self._configuration:
            if variable.name == key:
                return value
        raise KeyError("Instance '%s' has no value for variable '%s'!" % (self._name, key))



class Configuration(Visitee):


    def __init__(self, model, instances=None):
        self._instances = [each for each in instances]


    def resolve(self, identifier):
        for any_instance in self._instances:
            if any_instance.name == identifier:
                return any_instance
        raise KeyError("Unknown instance '{}'!".format(identifier))


    @property
    def instance_count(self):
        return len(self._instances)


    @property
    def instances(self):
        return self._instances


    @property
    def stacks(self):
        def top_services():
            for each in self.instances:
                if all(i.feature_provider is not each for i in self.instances):
                    yield each

        def stack_of(service):
            stack = [service]
            while stack[-1].feature_provider:
                stack.append(stack[-1].feature_provider)
            return stack

        for each_service in top_services():
            yield stack_of(each_service)



class Goals(object):


    def __init__(self, services=None, features=None):
        self._services = [each for each in services] \
                         if services else []
        self._features = [each for each in features] \
                         if features else []


    @property
    def services(self):
        return [each for each in self._services]


    @property
    def features(self):
        return [each for each in self._features]
