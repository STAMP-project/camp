#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from os.path import isfile, join as join_paths



class InvalidModel(Exception):

    def __init__(self, errors):
        self._errors = errors


    @property
    def errors(self):
        return self._errors



class Error(object):

    def __init__(self, problem, hint):
        self._problem = problem
        self._hint = hint


    def __repr__(self):
        return self.TEMPLATE % (self._problem, self._hint)

    TEMPLATE = ("Error: %s\n"
                "       %s\n")


    @property
    def hint(self):
        return self._hint


    @property
    def problem(self):
        return self._problem



class NoGoal(Error):

    def __init__(self):
        super(NoGoal, self).__init__(
            "No goal is defined.",
            "Define at least one running service.")



class NoServiceProvider(Error):
    PROBLEM = "No component provides the service '%s'!"
    HINT = "Do we miss a provided service or a component?"

    def __init__(self, service):
        super(NoServiceProvider, self).__init__(
            self.PROBLEM % service.name,
            self.HINT)



class NoFeatureProvider(Error):
    PROBLEM = "No component provides the feature '%s'!"
    HINT = "Do we miss a provided feature or a component?"

    def __init__(self, feature):
        super(NoFeatureProvider, self).__init__(
            self.PROBLEM % feature.name,
            self.HINT)



class EmptyVariableDomain(Error):


    def __init__(self, component, variable):
        super(EmptyVariableDomain, self).__init__(
            self.PROBLEM % (component.name, variable.name),
            self.HINT)

    PROBLEM = "Variable '%s::%s' has an empty domain!"
    HINT = "Variable must have at least one possible value."



class DockerFileNotFound(Error):

    def __init__(self, component, docker_file, workspace):
        super(DockerFileNotFound, self).__init__(
            self.PROBLEM % (docker_file, component.name),
            self.HINT % workspace)

    PROBLEM = "The Dockerfile '%s' of component '%s' cannot be found."
    HINT = "Is this the relative path from your workspace '%s'?"



class Checker(object):

    def __init__(self, workspace=None):
        self._workspace = workspace or "temp"
        self._errors = []


    def visit_model(self, model):
        self._errors = []
        self._at_least_one_service_or_feature(model)
        self._at_least_one_goal(model)

        for each_service in model.services:
            each_service.accept(self, model)

        for each_feature in model.features:
            each_feature.accept(self, model)

        for each_component in model.components:
            each_component.accept(self, model)

        if self._errors:
            raise InvalidModel(self._errors)


    def _at_least_one_service_or_feature(self, model):
        if len(model.services) == 0 and len(model.features) == 0:
            self._report(NoServiceAndNoFeature())


    def _at_least_one_goal(self, model):
        if len(model.goals.services) == 0 \
           and len(model.goals.features) == 0:
            self._report(NoGoal())


    def visit_service(self, service, model):
        self._exists_at_least_one_service_provider(model, service)


    def _exists_at_least_one_service_provider(self, model, service):
        for each_component in model.components:
            for any_provided_service in each_component.provided_services:
                if any_provided_service == service:
                    return True
        self._report(NoServiceProvider(service))


    def visit_feature(self, feature, model):
        self._exists_at_least_one_feature_provider(model, feature)


    def _exists_at_least_one_feature_provider(self, model, feature):
        for each_component in model.components:
            for any_provided_feature in each_component.provided_features:
                if any_provided_feature == feature:
                    return True
        self._report(NoFeatureProvider(feature))


    def visit_component(self, component, model):
        self._required_features_are_defined(model, component)
        self._provided_features_are_defined(model, component)
        self._required_services_are_defined(model, component)
        self._provided_services_are_defined(model, component)
        for each_variable in component.variables:
            each_variable.accept(self, model, component)
        if component.implementation:
            component.implementation.accept(self, model, component)


    def _required_features_are_defined(self, model, component):
        for any_feature in component.required_features:
            if not any_feature in model:
                self._report(UnknownRequiredFeature(model,
                                                    component,
                                                    any_feature))


    def _provided_features_are_defined(self, model, component):
        for any_feature in component.provided_features:
            if any_feature not in model:
                self._report(UnknownProvidedFeature(model,
                                                    component,
                                                    any_feature))


    def _required_services_are_defined(self, model, component):
        for any_service in component.required_services:
            if any_service not in model:
                self._report(UnknownRequiredService(model,
                                                    component,
                                                    any_service))


    def _provided_services_are_defined(self, model, component):
        for any_service in component.provided_services:
            if any_service not in model:
                self._report(UnknownProvidedService(model,
                                                    component,
                                                    any_service))


    def visit_variable(self, variable, model, component):
        if len(variable.domain) == 0 and variable.value_type != "Integer":
            self._report(EmptyVariableDomain(component, variable))


    def visit_dockerfile(self, dockerfile, model, component):
        path = join_paths(self._workspace, "template",  dockerfile.docker_file)
        if not isfile(path):
            self._report(DockerFileNotFound(component,
                                            path,
                                            self._workspace))


    def visit_dockerimage(self, dockerimage, model, component):
        pass


    def _report(self, new_error):
        self._errors.append(new_error)


    @property
    def errors(self):
        return self._errors
