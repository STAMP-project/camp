#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from setuptools import setup, find_packages

from camp import About



setup(name="camp",
      version=About.VERSION,
      description=About.DESCRIPTION,
      author="Hui Song",
      author_email="hui.song@sintef.no",
      url="https://github.com/STAMP-project/camp",
      packages=find_packages(exclude=["tests*", "tests.*"]),
      include_package_data = True,
      package_data = {
          "camp": ["data/metamodel.yml"]
      },
      license="MIT",
      test_suite="tests",
      entry_points = {
          'console_scripts': [
              'camp = camp.run:main'
          ]
      },
      install_requires = [
          "PyYAML == 5.1",
          "plumbum == 1.6.7",
          "jsonpath-rw == 1.4.0",
          "argparse == 1.2.1",
          "ozepy @ git+https://github.com/STAMP-project/ozepy.git@v1.0.0#egg=ozepy"
      ],
      tests_require=[
          "green==2.13.0",
          "mock==2.0.0",
          "deepdiff==3.3.0"
      ]
)
