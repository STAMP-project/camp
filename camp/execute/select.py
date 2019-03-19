#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.maven import MavenExecutor


SUPPORTED_TECHNOLOGIES =[
    ("maven", MavenExecutor)
]




def select_executor(technology, shell):

    for any_technology, factory in SUPPORTED_TECHNOLOGIES:
        if any_technology == technology:
            return factory(shell)

    raise TechnologyNotSupported(technology)



class TechnologyNotSupported(Exception):

    def __init__(self, technology):
        self._technology = technology

    @property
    def technology(self):
        return self._technology
