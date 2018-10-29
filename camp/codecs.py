#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from camp.entities.model import Model, Component, Service, Goals, Variable, Feature

from yaml import load



class YAMLCodec(object):


    def __init__(self):
        self._warnings = []


    def load_model_from(self, stream):
        data = load(stream)
        components = []
        goals = Goals()
        for key, item in data.items():
            if key == Keys.COMPONENTS:
                components = self._parse_components(item)

            elif key == Keys.GOALS:
                goals = self._parse_goals(item)

            else:
                self._warn(IgnoredEntry(key))

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

        for key, items in data.items():

            if key == Keys.PROVIDES_SERVICES:
                for each_name in data[Keys.PROVIDES_SERVICES]:
                    provided_services.append(Service(each_name))

            elif key == Keys.REQUIRES_SERVICES:
                for each_name in data[Keys.REQUIRES_SERVICES]:
                    required_services.append(Service(each_name))

            elif key == Keys.PROVIDES_FEATURES:
                for each_name in data[Keys.PROVIDES_FEATURES]:
                    provided_features.append(Feature(each_name))

            elif key == Keys.REQUIRES_FEATURES:
                for each_name in data[Keys.REQUIRES_FEATURES]:
                    required_features.append(Feature(each_name))

            elif key == Keys.VARIABLES:
                variables = self._parse_variables(data[Keys.VARIABLES])

            else:
                self._warn(IgnoredEntry(Keys.COMPONENTS, name, key))


        return Component(name,
                         provided_services=provided_services,
                         required_services=required_services,
                         provided_features=provided_features,
                         required_features=required_features,
                         variables=variables)


    def _parse_variables(self, data):
        variables = []
        for key, item in data.items():
            variables.append(self._parse_variable(key, item))
        return variables


    def _parse_variable(self, name, data):
        domain = []
        if Keys.DOMAIN in data:
            for each_value in data[Keys.DOMAIN]:
                domain.append(str(each_value))
        return Variable(name, domain)


    def _parse_goals(self, data):
        running_services = []
        for key, item in data.items():
            if key == Keys.RUNNING:
                for each_name in item:
                    running_services.append(Service(each_name))
            else:
                self._warn(IgnoredEntry(Keys.GOALS, key))
                
        return Goals(running_services)


    def _warn(self, warning):
        self._warnings.append(warning)


    @property
    def warnings(self):
        return self._warnings



class Keys:
    """
    The labels that are fixed in the YAML
    """

    COMPONENTS = "components"
    DOMAIN = "domain"
    GOALS = "goals"
    PROVIDES_FEATURES = "provides_features"
    PROVIDES_SERVICES = "provides_services"
    REQUIRES_FEATURES = "requires_features"
    REQUIRES_SERVICES = "requires_services"
    RUNNING = "running"
    VARIABLES = "variables"



class IgnoredEntry(object):


    def __init__(self, *path):
        self._path = '/'.join(path)


    @property
    def path(self):
        return self._path


    def __str__(self):
        return "Entry '%s' ignored!" % self._path
