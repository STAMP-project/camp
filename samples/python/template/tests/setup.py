#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from setuptools import setup


setup(name="test-greetings",
      version="1.0.0",
      description="Integration tests for the Greeting service",
      author="Franck Chauvel",
      author_email="franck.chauvel@sintef.no",
      py_modules=["integrations"],
      install_requires = [
          "requests",
          "green @ git+https://github.com/cleancut/green.git@master#egg=green"
      ]
)
