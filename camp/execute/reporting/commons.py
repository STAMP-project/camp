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



class ReportReader(object):


    def extract_from_text(self, text):
        raise NotImplementedError("ReportReader is an abstract class!")
