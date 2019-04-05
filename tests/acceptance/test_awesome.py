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



class FilesAreGenerated(CampTests):


    def setUp(self):
        self.sample = Sample("awesome")


    def test_generate_all(self):
        self.generate_all()
        self.assertEqual(6, len(self.sample.generated_configurations))


    def test_generate_coverage(self):
        self.generate_coverage()
        # /!\ FLAKY TEST: The number of configurations generated Z3
        # seems to vary, though it should always build 3
        # configurations. Check the build reports (e.g., #146)
        self.assertIn(len(self.sample.generated_configurations),
                      [3, 4])
