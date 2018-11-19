#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from tests.acceptance.commons import CampTests, Sample



class FilesAreGenerated(CampTests):


    def setUp(self):
        self.sample = Sample("awesome", self.WORKSPACE)


    WORKSPACE = "tmp/acceptance"


    def test_generate_all(self):
        self.generate_all()
        self.assertEqual(6, len(self.sample.generated_configurations))


    def test_generate_coverage(self):
        self.generate_coverage()
        self.assertEqual(3, len(self.sample.generated_configurations))
