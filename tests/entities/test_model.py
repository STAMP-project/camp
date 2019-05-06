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

from camp.entities.model import TestSettings, ResourceSelection

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
        self._resource = ["whatever.txt", "doesnt_matter.ini" ]
        self._selection = ResourceSelection(*self._resource)


    def test_expose_the_selected_resources(self):
        self.assertEqual(self._resource, self._selection.resources)


    def test_equal_itself(self):
        self.assertEqual(self._selection, self._selection)


    def test_differ_from_a_different_selection(self):
        other = ResourceSelection("something different")
        self.assertNotEqual(self._selection, other)


    def test_equal_another_identical_selection(self):
        other = ResourceSelection(*self._resource)
        self.assertEqual(self._selection, other)


    def test_have_the_same_hash_than_an_identical_resource(self):
        other = ResourceSelection(*self._resource)
        self.assertEqual(hash(self._selection), hash(other))


    def test_have_a_different_hash_from_an_identical_resource(self):
        other = ResourceSelection("whatever different")
        self.assertNotEqual(hash(self._selection), hash(other))
