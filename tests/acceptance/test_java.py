#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from tests.commons import CampTest, Scenario



class JavaGreetingsShould(CampTest):


    def setUp(self):
        self.scenario = Scenario.from_sample("java")


    def test_yield_three_configurations(self):
        self.generate_all()

        configurations = self.scenario.generated_configurations

        self.assertEqual(3, len(configurations))


    def test_run_all_tests_three_times(self):
        self.generate_all()
        self.realize()
        self.execute()

        report = self.scenario.fetch_test_report()

        self.assertEqual(3, len(report["reports"]))


    def test_run_only_configuration_number_two(self):
        self.generate_all()
        self.realize()
        self.execute(simulated=True, include=[2])

        report = self.scenario.fetch_test_report()

        self.assertEqual(1, len(report["reports"]))
