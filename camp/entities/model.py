#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



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
        assert name and type(name) == str, "name must be a string!"
        self._name = name


    @property
    def name(self):
        return self._name



class Model(Visitee):

    def __init__(self, components, goals):
        self._components = {each.name: each for each in components}
        self._goals = goals


    def resolve(self, identifier):
        if identifier in self._components:
            return self._components[identifier]

        for any_service in self.services:
            if any_service.name == identifier:
                return any_service

        for any_feature in self.features:
            if any_feature.name == identifier:
                return any_feature
            
        else:
            raise KeyError(identifier)


    def __contains__(self, object):
        kind = type(object)
        if kind == Feature:
            return object in self.features
        elif kind == Component:
            return object.name in self._components
        elif kind == Service:
            return object in self.services
        else:
            return None


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



class Service(NamedElement):
    """
    Immutable value object.
    """

    def __init__(self, name):
        super(Service, self).__init__(name)


    def __eq__(self, other):
        if type(other) != Service: return False
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
        if type(other) != Feature: return False
        return self._name == other.name


    def __repr__(self):
        return "Feature('%s')" % self._name


    def __hash__(self):
        return hash(self._name)



class Component(NamedElement):


    def __init__(self, name,
                 provided_features=[],
                 required_features=[],
                 provided_services=[],
                 required_services=[],
                 variables=[]):
        super(Component, self).__init__(name)
        self._required_features = [each for each in required_features]
        self._provided_features = [each for each in provided_features]
        self._required_services = [each for each in required_services]
        self._provided_services = [each for each in provided_services]
        self._variables = {each.name: each for each in variables}


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



class Variable(NamedElement):


    def __init__(self, name, values):
        super(Variable, self).__init__(name)
        self._values = [each for each in values]


    @property
    def domain(self):
        return [each for each in self._values]



class Instance(NamedElement):

    def __init__(self, name, definition):
        super(Instance, self).__init__(name)
        self._definition = definition
        self._feature_provider = None
        self._service_providers = []
        self._configuration = []

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



class Configuration(Visitee):


    def __init__(self, model, instances=[]):
        self._instances = {each.name:each for each in instances}


    def resolve(self, identifier):
        return self._instances[identifier]
    

    @property
    def instance_count(self):
        return len(self._instances)
    
    
    @property
    def instances(self):
        return [ each for each in self._instances.values() ]
    
    

class Goals(object):


    def __init__(self, services=[], features=[]):
        self._services = [each for each in services]
        self._features = [each for each in features]


    @property
    def services(self):
        return [each for each in self._services]


    @property
    def features(self):
        return [each for each in self._features]

