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



test_dependencies = [
    "green==2.14.2",
    "mock==2.0.0",
    "deepdiff==3.3.0",
    "coverage==4.5.3"
]

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
          "future == 0.17.1",
          "PyYAML == 5.1",
          "jsonpath-rw == 1.4.0",
          "argparse == 1.2.1",
          "ozepy @ git+https://github.com/STAMP-project/ozepy.git@v1.0.1#egg=ozepy"
      ],
      tests_require = test_dependencies,
      extras_require = {
          "test": test_dependencies
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Testing"
      ],
)
