#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from requests import get

from unittest import TestCase



class GreetingServiceShould(TestCase):


    def test_reply_OK(self):
        response = get(self.URL.format(user="franck"))
        self.assertEqual(200, response.status_code)

    URL = "http://greetings:5000/hello/{user}"
