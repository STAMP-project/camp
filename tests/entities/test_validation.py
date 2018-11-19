#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from unittest import TestCase

from camp.entities.model import Model, Service, Feature, Component, \
    Variable, Goals, DockerFile
from camp.entities.validation import *



class TestModelIsInvalid(TestCase):

    def setUp(self):
        self._components = [Component(name="c1",
                                      provided_services=[Service("S1")],
                                      provided_features=[Feature("F1")])]
        self._goals = Goals(services=[Service("S1")])
        self._errors = []


    def test_when_no_goal_is_given(self):
        self._goals = Goals()

        self._validate_model()

        self._verify_errors(NoGoal)


    def test_when_no_one_provides_a_required_service(self):
        self._components = [Component(name="c1",
                                      provided_services=[Service("Awesome")])]

        self._validate_model()

        self._verify_errors(NoServiceProvider)


    def test_when_no_one_provides_a_required_feature(self):
        self._components.append(Component(name="c2",
                                          required_features=[Feature("Awesome")]))

        self._validate_model()

        self._verify_errors(NoFeatureProvider)


    def test_when_a_variable_has_no_value(self):
        self._components = [Component(name="c1",
                                      provided_services=[Service("S1")],
                                      provided_features=[Feature("F1")],
                                      variables=[Variable("memory", str, [])])
        ]

        self._validate_model()

        self._verify_errors(EmptyVariableDomain)

        
    def test_when_a_docker_file_does_not_exists(self):
        self._components = [Component(name="c1",
                                      provided_services=[Service("S1")],
                                      implementation=DockerFile("this/file/does_not_exist"))]

        self._validate_model()

        self._verify_errors(DockerFileNotFound)


    def _verify_errors(self, *expected_errors):
        self.assertEqual(len(expected_errors), len(self._errors), str(self._errors))
        for each_error in expected_errors:
            self.assertTrue(isinstance(e, each_error) for e in self._errors)


    def _validate_model(self):
        model =  Model(components=self._components,
                       goals=self._goals)
        checker = Checker()
        model.accept(checker)
        self._errors = checker.errors
