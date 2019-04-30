#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.entities.model import Variable

from unittest import TestCase



class FindMaximumCoverageSmallerOrEqualToTheRequestedOne(TestCase):


    def _assertItemsEqual(self, expected, actual):
        # For compatibility with Python 2.7, as the method
        # assertItemsEquals has been renamed in Python 3.3 into
        # 'assertCountEqual'.
        return self.assertEqual(sorted(expected), sorted(actual))


    def test_given_the_minimum_coverage(self):
        values = Variable.cover(0, 6, 1)

        self._assertItemsEqual([0, 1, 2, 3, 4, 5, 6],
                              values)


    def test_given_a_coverage_that_is_a_natural_divisor(self):
        values = Variable.cover(0, 6, 3)

        self._assertItemsEqual([0, 3, 6],
                              values)


    def test_given_a_coverage_that_is_not_a_natural_divisor(self):
        values = Variable.cover(0, 6, 4)

        self._assertItemsEqual([0, 3, 6],
                              values)


    def test_given_the_maximum_coverage(self):
        values = Variable.cover(0, 6, 6)

        self._assertItemsEqual([0, 6],
                              values)


    def test_given_a_coverage_above_the_maximum_coverage(self):
        values = Variable.cover(0, 6, 7)

        self._assertItemsEqual([0, 6],
                              values)


    def test_given_a_coverage_way_above_the_maximum_coverage(self):
        values = Variable.cover(0, 6, 12)

        self._assertItemsEqual([0, 6],
                              values)
