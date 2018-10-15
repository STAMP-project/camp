#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from setuptools import setup

from camp import ABOUT


setup(name="camp",
      version=About.VERSION,
      description=About.DESCRIPTION,
      author="Hui Song",
      author_email="hui.song@sintef.no",
      url="https://github.com/STAMP-project/camp",
      packages=["camp"],
      license="MIT",
      test_suite="tests",
      entry_points = {
          'console_scripts': [
              'camp = camp.main:start'
          ]
      }
)
