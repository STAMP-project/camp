#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp import __VERSION__, __COPYRIGHT__, __LICENSE__



def start():
    print "CAMP v%s (%s)" % (__VERSION__, __LICENSE__)
    print __COPYRIGHT__
