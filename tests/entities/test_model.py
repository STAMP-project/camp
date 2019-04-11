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

from camp.entities.model import TestSettings

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
                         self._settings.run_tests_command)


    def test_expose_the_format_of_test_reports(self):
        self.assertEqual(self._report_format,
                         self._settings.report_format)


    def test_expose_the_location_of_the_reports(self):
        self.assertEqual(self._report_location,
                         self._settings.report_location)


    def test_expose_a_pattern_to_detect_test_report(self):
        self.assertEqual(self._report_pattern,
                         self._settings.report_pattern)
