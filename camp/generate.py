#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Configuration, Instance, Component

from ozepy import load_all_classes, DefineObject, ObjectVar, Not, \
    get_all_meta_facts, get_all_config_facts, cast_all_objects, \
    generate_config_constraints, generate_meta_constraints, start_over

from pkgutil import get_data

from yaml import load as load_yaml

from z3 import Optimize, sat



class Z3Problem(object):


    @staticmethod
    def from_model(model):
        start_over()
        import ozepy, z3
        reload(ozepy)
        reload(z3)
        context = Context()
        context.load_metamodel()
        context.load_model(model)

        solver = Optimize()

    
        generate_meta_constraints()
        generate_config_constraints()

        solver.add(*get_all_meta_facts())
        solver.add(*get_all_config_facts())

        context.declare(INTEGRITY_VARIABLES)

        for each_constraint in INTEGRITY_CONSTRAINTS:
            solver.add(context.evaluate(each_constraint.strip()))

        for each_running_service in model.goals.services:
            constraint = RUNNING_SERVICE.format(each_running_service.name)
            solver.add(context.evaluate(constraint.strip()))
            
        return Z3Problem(model, context, solver)


    def __init__(self, model, context, solver):
        self._model = model
        self._context = context
        self._solver = solver


    def all_solutions(self):
        while self.has_solution():
            yield self.solve()

    def has_solution(self):
        return self._solver.check() == sat


    def solve(self):
        z3_solution = cast_all_objects(self._solver.model())

        #import pprint ; pprint.pprint(z3_solution)
            
        self._solver.add(self._context.evaluate(self._as_constraint(z3_solution)))
        return self._extract_from(z3_solution)


    def _as_constraint(self, z3_solution):
        clauses = []
        for key, item in z3_solution.items():
            if "use_feature" in item:
                if item["use_feature"] is not None:
                    clauses.append("%s.use_feature != %s" % \
                                   (key, item["use_feature"]))
                if item["use_services"]:
                    for each_provider in item["use_services"]:
                        clauses.append("Not(%s.use_services.contains(%s))" %
                                   (key, each_provider))
                if item["configuration"]:
                    for each_value in item["configuration"]:
                        clauses.append("Not(%s.configuration.contains(%s))" %\
                                   (key, each_value))
        return "Or(" + ",".join(clauses) + ")"


    def _extract_from(self, z3_solution):
        instances = []
        for key, item in z3_solution.items():
            if "definition" in item:
                component = self._model.resolve(item["definition"])
                instances.append(Instance(item["name"], component))

        result = Configuration(self._model, instances)

        for key, item in z3_solution.items():
            if "definition" in item:
                instance = result.resolve(item["name"])
                if "use_feature" in item and item["use_feature"]:
                    provider = result.resolve(item["use_feature"])
                    instance.feature_provider = provider
                if "use_services" in item:
                    providers = [result.resolve(each) \
                                 for each in item["use_services"]]
                    instance.service_providers = providers
                if "configuration" in item:
                    configuration = []
                    for each_value in item["configuration"]:
                        for any_variable in instance.definition.variables:
                            for any_value in any_variable.domain:
                                if any_variable.name in each_value \
                                   and any_value in each_value:
                                    configuration.append((any_variable, any_value))
                    instance.configuration = configuration

        return result



class Context(object):

    def __init__(self):
        self._definitions = {}
        exec("from ozepy import Not, Implies, Or, And", self._definitions)


    def evaluate(self, constraint):
        return eval(constraint, self._definitions)


    def declare(self, declarations):
        for type_name, variables in declarations:
            for variable_name in variables:
                self.define(variable_name, ObjectVar(self.find(type_name),
                                                     variable_name))


    def load_metamodel(self):
        data = get_data('camp', 'data/metamodel.yml')
        metamodel = load_yaml(data)
        metaclasses = load_all_classes(metamodel)
        for each in metaclasses:
            self._definitions[each.name] = each


    def load_model(self, model):
        self._define_all_services(model)
        self._define_all_features(model)
        self._define_all_components(model)


    def _define_all_services(self, model):
        for each_service in model.services:
            z3_service = DefineObject(each_service.name,
                                      self.find("Service"))
            self.define(each_service.name, z3_service)


    def _define_all_features(self, model):
        for each_feature in model.features:
            z3_feature = DefineObject(each_feature.name,
                                      self.find("Feature"))
            self.define(each_feature.name, z3_feature)


    def _define_all_components(self, model):
        for each_component in model.components:
            z3_component = DefineObject(each_component.name,
                                        self.find("Component"))
            self.define(each_component.name, z3_component)

            self._define_all_variables(each_component)

            provide_services = [self.find(each.name) \
                                for each in each_component.provided_services]
            z3_component.force_value("provide_services", provide_services)

            require_services = [self.find(each.name) \
                                for each in each_component.required_services]
            z3_component.force_value("require_services", require_services)

            provide_features = [self.find(each.name) \
                                for each in each_component.provided_features]
            z3_component.force_value("provide_features", provide_features)

            require_features = [self.find(each.name) \
                                for each in each_component.required_features]
            z3_component.force_value("require_features", require_features)

            settings = [self.find(self.qualified_name(each_component.name,
                                                      each.name)) \
                        for each in each_component.variables]
            z3_component.force_value("settings", settings)

            self._instantiate(each_component, 1)


    def _define_all_variables(self, component):
        for each_variable in component.variables:
            qualified_name = self.qualified_name(component.name,
                                                 each_variable.name)

            z3_variable = DefineObject(qualified_name,
                                       self.find("Variable"))
            self.define(qualified_name, z3_variable)

            domain = []
            for each_value in each_variable.domain:
                qualified_name = self.qualified_name(component.name,
                                                     each_variable.name,
                                                     each_value)
                z3_value = DefineObject(qualified_name,
                                        self.find("Value"))
                domain.append(z3_value)
                self.define(qualified_name, z3_value)
                z3_variable.force_value("domain", domain)


    def qualified_name(self, *parts):
        return "_".join(parts)


    def _instantiate(self, component, count=1):
        for index in range(count):
            instance_name = component.name.lower() + "_%d" % index
            z3_instance = DefineObject(instance_name,
                                       self.find("CInstance"),
                                       suspended=True)
            self.define(instance_name, z3_instance)
            z3_instance.force_value("definition", self.find(component.name))


    def define(self, key, value):
        assert key not in self._definitions, \
            "'%s' has already been defined!" % key
        self._definitions[key] = value


    def find(self, identifier):
        return self._definitions[identifier]


    def __contains__(self, identifier):
        return identifier in self._definitions



INTEGRITY_VARIABLES = [
    ("CInstance", ["ci", "spi"]),
    ("Feature", ["fr", "fp"]),
    ("Service", ["sr", "sp"]),
    ("Variable", ["var"]),
    ("Value", ["val"])
]


INTEGRITY_CONSTRAINTS = [
    # There must be at least one instance
    """
    CInstance.all_instances().count() > 0
    """,

    # Cannot be deploy on itself
    """
    CInstance.forall(ci, Not(ci["use_feature"] == ci))
    """,

    # Cannot use its own services
    """
    CInstance.forall(ci, Not(ci["use_services"].exists(
           spi, spi == ci)))
    """,

    # Can only deploy on something that provides the required features
    """
    CInstance.forall(ci, ci["definition"]["require_features"].forall(
    fr, ci.use_feature["definition"].provide_features.exists(fp, fp == fr)))
    """,

    # Can only connect to something that provides the required services
    """
    CInstance.forall(ci, ci["definition"]["require_services"].forall(
    sr, ci["use_services"].exists(
    spi, spi["definition"]["provide_services"].contains(sr))))
    """,

    # Should have a value for each setting defined in its definition
    """
    CInstance.forall(ci, 
       ci["definition"]["settings"].forall(var, 
          ci["configuration"].exists(val, 
             var["domain"].contains(val))))
    """,

    # Each variable in the component settings should have one
    # corresponding value in the instance configuration
    """
    CInstance.forall(ci,
       ci.definition.settings.forall(var,
          ci.configuration.filter(val, var.domain.contains(val)).count() == 1))
    """,

    # Each value in the instance configuration should have one
    # corresponding variable in the component settings
    """
    CInstance.forall(ci,
       ci.configuration.forall(val,
          ci.definition.settings.filter(var, var.domain.contains(val)).count() == 1))
    """,


    # Instances that do not require services cannot have any
    # service provider
    """
    CInstance.forall(ci, Implies(
       ci["definition"]["require_services"].count() == 0,
       ci["use_services"].count() == 0))
    """,

    # Instances that do not require features cannot have any
    # feature_provider
    """
    CInstance.forall(ci, Implies(ci["definition"]["require_features"].count() == 0,
    ci["use_feature"].undefined()))
    """,

    # Instances that do require features must have any
    # feature_provider
    """
    CInstance.forall(ci, Implies(ci["definition"]["require_features"].count() > 0,
    Not(ci["use_feature"].undefined())))
    """
]


RUNNING_SERVICE = """CInstance.filter(ci, ci["definition"].provide_services.exists
( sp, sp == {})).count() == 1"""
