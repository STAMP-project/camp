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



class FilesAreGenerated(CampTest):


    def setUp(self):
        self.scenario = Scenario.from_sample("awesome")


    def test_generate_all(self):
        self.generate_all()
        self.assertEqual(6, len(self.scenario.generated_configurations))


    def test_generate_coverage(self):
        self.generate_coverage()
        # /!\ FLAKY TEST: The number of configurations generated Z3
        # seems to vary, though it should always build 3
        # configurations. Check the build reports (e.g., #146)
        self.assertIn(len(self.scenario.generated_configurations),
                      [3, 4])
