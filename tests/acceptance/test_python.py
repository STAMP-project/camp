#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from tests.acceptance.commons import CampTests, Sample



class PythonGreetingsShould(CampTests):


    def setUp(self):
        self.sample = Sample("python")


    def test_yield_nine_configurations(self):
        self.generate_all()

        configurations = self.sample.generated_configurations

        self.assertEqual(9, len(configurations))


    def test_run_all_tests_nine_times(self):
        self.generate_all()
        self.realize()
        self.execute()

        report = self.sample.fetch_test_report()

        self.assertEqual(9, len(report["reports"]))
