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

from camp.entities.model import TestSettings, ResourceSelection, \
    ComponentResourceSelection

from unittest import TestCase



class TheTestSettingsShould(TestCase):


    def setUp(self):
        self._command = "this is a Shell command"
        self._report_format = "JUnit"
        self._report_location = "in/this/directory"
        self._report_pattern = "TEST*.xml"
        self._settings = TestSettings(
            self._command,
            self._report_format,
            self._report_location,
            self._report_pattern
        )


    def test_expose_a_command_to_run_the_tests(self):
        self.assertEqual(self._command,
                         self._settings.test_command)


    def test_expose_the_format_of_test_reports(self):
        self.assertEqual(self._report_format,
                         self._settings.report_format)


    def test_expose_the_location_of_the_reports(self):
        self.assertEqual(self._report_location,
                         self._settings.report_location)


    def test_expose_a_pattern_to_detect_test_report(self):
        self.assertEqual(self._report_pattern,
                         self._settings.report_pattern)


class ResourceSelectionsShould(TestCase):

    def setUp(self):
        self._destination = "file.txt"
        self._resources = ["whatever.txt", "doesnt_matter.ini" ]
        self._selection = ResourceSelection(self._destination,
                                            self._resources)

    def test_expose_the_selected_resources(self):
        self.assertEqual(self._resources,
                         self._selection.resources)


    def test_expose_its_destination(self):
        self.assertEqual(self._destination,
                         self._selection.destination)


    def test_equal_itself(self):
        self.assertEqual(self._selection, self._selection)


    def test_differ_from_a_selection_with_a_different_resources(self):
        other = ResourceSelection(self._destination,
                                  ["resource_1.txt", "resource_2.txt"])
        self.assertNotEqual(self._selection, other)


    def test_differ_from_a_selection_with_a_different_destination(self):
        other = ResourceSelection("something_different.txt",
                                  self._resources)
        self.assertNotEqual(self._selection, other)


    def test_equal_another_identical_selection(self):
        twin = ResourceSelection(self._destination,
                                  self._resources)
        self.assertEqual(self._selection, twin)


    def test_have_the_same_hash_than_an_identical_resource(self):
        twin = ResourceSelection(self._destination,
                                  self._resources)
        self.assertEqual(hash(self._selection), hash(twin))


    def test_have_a_different_hash_from_a_selection_with_different_resource(self):
        other = ResourceSelection(self._destination,
                                  ["resource_1.txt", "resource_2.txt"])
        self.assertNotEqual(hash(self._selection), hash(other))


    def test_have_a_different_hash_from_a_selection_with_a_different_destination(self):
        other = ResourceSelection("something_different.txt",
                                  self._resources)
        self.assertNotEqual(hash(self._selection), hash(other))



class ComponentResourceSelectionShould(TestCase):

    def setUp(self):
        self._selected_resource = "foo_config.ini"
        self._alternatives = set([
            "bar_config.ini",
            "quz_config.ini"])
        self._alias = "config.ini"
        self._selection = ComponentResourceSelection(
            self._selected_resource,
            self._alternatives,
            self._alias)


    def test_expose_the_selected_resource(self):
        self.assertEquals(self._selection.selected_resource,
                          self._selected_resource)


    def test_expose_the_candidates_resources(self):
        self.assertEquals(self._selection.alternatives,
                          self._alternatives)


    def test_expose_the_desired_alias(self):
        self.assertEquals(self._selection.alias,
                          self._alias)


    def test_detect_selected_resource_appears_in_alternatives(self):
        with self.assertRaises(ValueError):
            ComponentResourceSelection("foo.ini",
                                       ["foo.ini", "quz.ini"],
                                       "prout.ini")

    def test_use_the_selected_resource_as_alias_if_none_given(self):
        selection = ComponentResourceSelection(self._selected_resource,
                                               self._alternatives)
        self.assertEquals(selection.alias,
                          self._selected_resource)

    # Test the equality

    def test_equals_itself(self):
        self.assertEquals(self._selection, self._selection)


    def test_equals_a_similiar_resource_selection(self):
        other = ComponentResourceSelection(self._selected_resource,
                                           self._alternatives,
                                           self._alias)
        self.assertEquals(self._selection, other)


    def test_differs_when_selected_resource_are_different(self):
        other = ComponentResourceSelection("something_else",
                                           self._alternatives,
                                           self._alias)
        self.assertNotEquals(other, self._selection)


    def test_differs_when_alternatives_are_different(self):
        other = ComponentResourceSelection(self._selected_resource,
                                           ["bar.ini"],
                                           self._alias)
        self.assertNotEquals(other, self._selection)


    def test_differs_when_aliases_are_different(self):
        other = ComponentResourceSelection(self._selected_resource,
                                           self._alternatives,
                                           "something_different")
        self.assertNotEquals(other, self._selection)


    def test_has_the_same_hash_than_similar_selection(self):
        other = ComponentResourceSelection(self._selected_resource,
                                           self._alternatives,
                                           self._alias)
        self.assertEquals(hash(self._selection), hash(other))


    def test_has_a_differen_hash_when_selected_resources_vary(self):
        other = ComponentResourceSelection("something_different",
                                           self._alternatives,
                                           self._alias)
        self.assertNotEquals(hash(self._selection), hash(other))


    def test_has_a_differen_hash_when_alternatives_vary(self):
        other = ComponentResourceSelection(self._selected_resource,
                                           ["something", "different"],
                                           self._alias)
        self.assertNotEquals(hash(self._selection), hash(other))


    def test_has_a_differen_hash_when_aliases_vary(self):
        other = ComponentResourceSelection(self._selected_resource,
                                           self._alternatives,
                                           "something.different")
        self.assertNotEquals(hash(self._selection), hash(other))
