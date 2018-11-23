#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Configuration, Instance
from camp.util import redirect_stderr_to

from ozepy import load_all_classes, DefineObject, ObjectVar, \
    get_all_meta_facts, get_all_config_facts, cast_all_objects, \
    generate_config_constraints, generate_meta_constraints, start_over, \
    ObjectConst

from pkgutil import get_data
from pprint import pprint

from yaml import load as load_yaml

from z3 import Optimize, sat



class Z3Problem(object):


    @staticmethod
    def from_model(model):
        start_over()
        context = Context()
        context.load_metamodel()
        context.load_model(model)

        solver = Optimize()

        generate_meta_constraints()
        generate_config_constraints()

        solver.add(*get_all_meta_facts())
        solver.add(*get_all_config_facts())

        context.declare(INTEGRITY_VARIABLES)
        context.declare_helper_functions()

        for each_constraint in INTEGRITY_CONSTRAINTS:
            solver.add(context.evaluate(each_constraint))

        for each_running_service in model.goals.services:
            constraint = RUNNING_SERVICE.format(each_running_service.name)
            solver.add(context.evaluate(constraint))

        for each_constraint in model.constraints:
            solver.add(context.evaluate(each_constraint))

        for each_constraint in context.value_constraints:
            solver.add(context.evaluate(each_constraint))

        #print solver.sexpr()
        return Z3Problem(model, context, solver)



    def __init__(self, model, context, solver):
        self._model = model
        self._context = context
        self._solver = solver


    @redirect_stderr_to("z3_errors.log")
    def all_solutions(self):
        self._solver.push()
        while self.has_solution():
            yield self._solve()


    @redirect_stderr_to("z3_errors.log")
    def coverage(self):
        self._solver.push()
        while self.has_solution():
            yield self._cover()


    def has_solution(self):
        return self._solver.check() == sat


    def _cover(self):
        z3_solution = cast_all_objects(self._solver.model())
        #pprint(z3_solution)

        self._context.mark_as_covered(z3_solution)

        self._solver.pop()
        self._solver.push()
        self._solver.add(self._context.evaluate(self._as_constraint(z3_solution)))
        self._solver.push()
        self._solver.add(self._context.coverage_constraint())
        self._solver.maximize(self._context.coverage_gain())
        return self._extract_from(z3_solution)


    def _solve(self):
        z3_solution = cast_all_objects(self._solver.model())

        self._solver.add(self._context.evaluate(self._as_constraint(z3_solution)))
        return self._extract_from(z3_solution)


    @staticmethod
    def _as_constraint(z3_solution):
        clauses = []
        for key, item in z3_solution.items():
            if "use_feature" in item:
                if item["use_feature"] is not None:
                    clauses.append("%s.use_feature != %s" % \
                                   (key, item["use_feature"]))
                if item["partners"]:
                    for each_partner in item["partners"]:
                        clauses.append("%s.endpoint != %s" %
                                   (each_partner, z3_solution[each_partner]["endpoint"]))
                if item["configuration"]:
                    for each_value in item["configuration"]:
                        clauses.append("Not(%s.value == %s)" %\
                                       (each_value, z3_solution[each_value]["value"]))
        return "Or(" + ",".join(clauses) + ")"



    def _extract_from(self, z3_solution):
        instances = []
        for _, item in z3_solution.items():
            if "definition" in item:
                component = self._model.resolve(item["definition"])
                instances.append(Instance(item["name"], component))

        result = Configuration(self._model, instances)

        for _, item in z3_solution.items():
            if "definition" in item:
                instance = result.resolve(item["name"])
                if "use_feature" in item and item["use_feature"]:
                    provider = result.resolve(item["use_feature"])
                    instance.feature_provider = provider
                if "partners" in item:
                    providers = [result.resolve(z3_solution[each]["endpoint"]) \
                                 for each in item["partners"]]
                    instance.service_providers = providers
                if "configuration" in item:
                    configuration = []
                    for each_value in item["configuration"]:
                        variable_name = z3_solution[each_value]["variable"]
                        variable = None
                        for any_variable in instance.definition.variables:
                            if variable_name.endswith(any_variable.name):
                                variable = any_variable
                                break
                        else:
                            raise KeyError("Component '%s' has no variable named '%s'" %
                                           (instance.definition.name,
                                            variable_name))
                        value = variable.value_at(z3_solution[each_value]["value"])
                        configuration.append((variable, value))
                    instance.configuration = configuration
        return result



class Context(object):

    def __init__(self):
        self._definitions = {}
        self._definitions[self.COVERED_VALUES] = []
        self._definitions[self.COVERED_COMPONENTS] = []
        exec("from ozepy import Not, Implies, Or, And", self._definitions)
        self._value_constraints = []

    COVERED_VALUES = "covered_values"
    COVERED_COMPONENTS = "covered_components"


    @property
    def value_constraints(self):
        return self._value_constraints


    def evaluate(self, constraint):
        #print constraint.strip()
        return eval(constraint.strip(), self._definitions)



    def declare(self, declarations):
        for type_name, variables in declarations:
            for variable_name in variables:
                self.define(variable_name, ObjectVar(self.find(type_name),
                                                     variable_name))

    def declare_helper_functions(self):
        def variable_helper(component_name, variable_name):
            variable_name = self.qualified_name(component_name, variable_name)
            variable_object = self.find(variable_name)
            return variable_object

        self.define("variable", variable_helper)


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
                                      self.find("Service"), suspended=True)
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


    @staticmethod
    def qualified_name(*parts):
        return "_".join(parts)


    def _instantiate(self, component, count=1):
        for index in range(count):
            instance_name = component.name.lower() + "_%d" % index
            z3_instance = DefineObject(instance_name,
                                       self.find("CInstance"),
                                       suspended=True)
            self.define(instance_name, z3_instance)
            z3_instance.force_value("definition", self.find(component.name))

            # define partners
            partners = []
            for each_required_service in component.required_services:
                partner_name = self.qualified_name(instance_name,
                                                   each_required_service.name)

                z3_partner = DefineObject(partner_name,
                                          self.find("Partner"),
                                          suspended=True)
                self.define(partner_name, z3_partner)
                partners.append(z3_partner)

                z3_partner.force_value("service",
                                       self.find(each_required_service.name))

            z3_instance.force_value("partners", partners)


            values = []
            for each_variable in component.variables:
                qualified_variable_name = "%s_%s" % (component.name, each_variable.name)
                value_name = "%s_%s" % (instance_name, each_variable.name)
                z3_value = DefineObject(value_name,
                                        self.find("Value"),
                                        suspended=True)
                self.define(value_name, z3_value)

                if each_variable.domain:
                    if each_variable.value_type != "Integer":
                        self._value_constraints.append(
                            "And([%s.value >= 0, %s.value < %d])" % (value_name,
                                                                     value_name,
                                                                     len(each_variable.domain)))
                    else:
                        clauses = ",".join("%s.value == %d" %
                                           (value_name, v) for v in each_variable.domain)
                        self._value_constraints.append("Or([" + clauses + "])")

                z3_value.force_value("variable", self.find(qualified_variable_name))

                values.append(z3_value)
            z3_instance.force_value("configuration", values)


    def define(self, key, value):
        if key in self._definitions:
            raise AssertionError("'%s' has already been defined!" % key)
        self._definitions[key] = value


    def find(self, identifier):
        return self._definitions[identifier]


    def __contains__(self, identifier):
        return identifier in self._definitions


    @property
    def covered_components(self):
        return self.find(self.COVERED_COMPONENTS)


    @property
    def covered_values(self):
        return self.find(self.COVERED_VALUES)


    def mark_as_covered(self, z3_solution):
        for key, item in z3_solution.items():
            if "definition" in item:
                definition = self.find(item["definition"])
                if not definition in self.covered_components:
                    self.covered_components.append(definition)
                if "configuration" in item:
                    for each_value in item["configuration"]:
                        value = z3_solution[each_value]
                        if not value in self.covered_values:
                           self.covered_values.append((value["variable"], value["value"]))

    def coverage_constraint(self):
        template = ("Or([CInstance.exists(ci, ci.configuration.exists(val, And([%s]))),"
                    "CInstance.exists(ci, And([%s]))])")
        values = ", ".join("Implies(val.variable == %s, val.value != %d)" % (variable, value) \
                          for variable, value in self.covered_values)
        components = ", ".join("ci.definition != %s" % each \
                              for each in self.covered_components)
        constraint = template % (values, components)
        return self.evaluate(constraint)


    def coverage_gain(self):
        constraint = "0"
        if self.covered_values:
            constraint = "CInstance.filter(ci, ci.configuration.exists(val, And([%s]))).count()"
            values = ", ".join("Implies(val.variable != %s, val.value != %d)" % (variable, value) \
                           for variable, value in self.covered_values)
            constraint = constraint % values
        constraint += " + CInstance.filter(ci, And([%s])).count()"
        components = ", ".join("ci.definition != %s" % each for each in self.covered_components)
        constraint = constraint % components
        return self.evaluate(constraint)



INTEGRITY_VARIABLES = [
    ("CInstance", ["ci", "ci1", "ci2", "spi"]),
    ("Feature", ["fr", "fp"]),
    ("Partner", ["partner"]),
    ("Service", ["service", "sr", "sp"]),
    ("Variable", ["var"]),
    ("Value", ["val", "val1", "val2"]),
    ("Component", ["cp"])
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

    # An instance cannot use its own services
    """
    CInstance.forall(ci, Not(ci.partners.exists(
           partner, partner.endpoint == ci)))
    """,

    # Can only deploy on something that provides the required features
    """
    CInstance.forall(ci, ci["definition"]["require_features"].forall(
    fr, ci.use_feature["definition"].provide_features.exists(fp, fp == fr)))
    """,

    # All partner shall connect to an endpoint that provides the requested service
    """
    Partner.forall(partner,
       partner.endpoint.definition.provide_services.exists(service,
          service == partner.service))
    """,

    # Instances that do not require services cannot have any
    # service provider
    """
    CInstance.forall(ci, Implies(
       ci["definition"]["require_services"].count() == 0,
       ci["partners"].count() == 0))
    """,

    # Instances that do not require features cannot have a
    # feature_provider
    """
    CInstance.forall(ci, Implies(ci["definition"]["require_features"].count() == 0,
    ci["use_feature"].undefined()))
    """,

    # Instances that do require features must have one
    # feature_provider
    """
    CInstance.forall(ci, Implies(ci["definition"]["require_features"].count() > 0,
    Not(ci["use_feature"].undefined())))
    """,

    # All provided features must be used
    """
    CInstance.forall(ci1,
       Implies(ci1.definition.provide_features.count() > 0,
               CInstance.exists(ci2, ci2.use_feature == ci1)))
    """,

    # Only one pending service
    """
    CInstance.filter(ci1,
          And([ci1.definition.provide_services.count() > 0,
               CInstance.forall(ci2, ci2.partners.forall(partner,
                    partner.endpoint != ci1))])).count() == 1
    """

    # No pending instances
    # """
    # CInstance.forall(ci1,
    #     Or([
    #       Not(ci1.use_feature.undefined()),
    #       ci1.partners.count() > 0,
    #       CInstance.exists(ci2,
    #           Or([ci2.use_feature == ci1,
    #               ci2.partners.exists(partner, partner.endpoint == ci1)]))]))
    # """
]


RUNNING_SERVICE = """CInstance.filter(ci, ci["definition"].provide_services.exists
( sp, sp == {})).count() == 1"""
