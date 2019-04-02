#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.util import redirect_stderr_to

from io import StringIO

from os import remove
from os.path import isfile

from unittest import TestCase

from sys import stderr



class RedirectionWorks(TestCase):


    def setUp(self):
        self._destination = "bidon.txt"
        self._message = "It works!\n"


    def tearDown(self):
        if isfile(self._destination):
            remove(self._destination)


    def test_with_a_redirection_to_a_file(self):

        @redirect_stderr_to(self._destination)
        def dummy_function():
            stderr.write(self._message)

        dummy_function()

        with open(self._destination, "r") as destination:
            content = destination.read()
            self.assertEqual(self._message, content)
