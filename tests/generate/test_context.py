#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from unittest import TestCase

from camp.entities.model import Model, Component, Service, Feature, Variable, Goals
from camp.generate import Context

from ozepy import start_over



class LoadedContextIncludes(TestCase):

    def setUp(self):
        start_over()
        self._context = Context()
        components = [
            Component("c1",
                      provided_services=[Service("S1")],
                      provided_features=[Feature("F1")],
                      variables=[Variable("memory",
                                          str,
                                          values=["1GB",
                                                  "2GB"])])
        ]
        self._model = Model(components,
                      Goals(services=[Service("S1")]))
        self._context.load_metamodel()
        self._context.load_model(self._model)

            
    def test_all_metaclasses(self):        
        for each in self.EXPECTED_CLASSES:
            self.assertIn(each, self._context)

    EXPECTED_CLASSES = ["Value", "Variable", "Service",
                        "Feature", "Component", "CInstance"]

    
    def test_all_services(self):
        for each in self._model.services:
            self.assertIn(each.name, self._context)

    def test_all_features(self):
        for each in self._model.features:
            self.assertIn(each.name, self._context)

    def test_all_components(self):
        for each in self._model.components:
            self.assertIn(each.name, self._context)

    def test_all_variables_with_qualified_names(self):
        for each_component in self._model.components:
            for each_variable in each_component.variables:
                qualified_name = "_".join([each_component.name, each_variable.name])
                self.assertIn(qualified_name, self._context)

    def test_all_values_slots_with_qualified_names(self):
        for each_component in self._model.components:
            for each_variable in each_component.variables:
                qualified_name = "_".join([each_component.name, "0", each_variable.name])
                self.assertIn(qualified_name, self._context)
                    
