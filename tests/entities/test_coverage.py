#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Variable

from unittest import TestCase



class FindMaximumCoverageSmallerOrEqualToTheRequestedOne(TestCase):


    def test_given_the_minimum_coverage(self):
        values = Variable.cover(0, 6, 1)

        self.assertItemsEqual([0, 1, 2, 3, 4, 5, 6],
                              values)


    def test_given_a_coverage_that_is_a_natural_divisor(self):
        values = Variable.cover(0, 6, 3)

        self.assertItemsEqual([0, 3, 6],
                              values)


    def test_given_a_coverage_that_is_not_a_natural_divisor(self):
        values = Variable.cover(0, 6, 4)

        self.assertItemsEqual([0, 3, 6],
                              values)


    def test_given_the_maximum_coverage(self):
        values = Variable.cover(0, 6, 6)

        self.assertItemsEqual([0, 6],
                              values)


    def test_given_a_coverage_above_the_maximum_coverage(self):
        values = Variable.cover(0, 6, 7)

        self.assertItemsEqual([0, 6],
                              values)


    def test_given_a_coverage_above_the_maximum_coverage(self):
        values = Variable.cover(0, 6, 12)

        self.assertItemsEqual([0, 6],
                              values)

