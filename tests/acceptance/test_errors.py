#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from tests.acceptance.commons import Sample, CampTests


class MissingCAMPModelIsReported(CampTests):

    
    def setUp(self):
        self.sample = Sample("no_camp_model", self.WORKSPACE)

    WORKSPACE = "tmp/acceptance/errors"


    def test_when_we_generate_all(self):
        self.generate_all()
        

    
