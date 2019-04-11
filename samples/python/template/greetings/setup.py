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


setup(name="greetings",
      version="1.0.0",
      description="Sample Greeting Service",
      author="Franck Chauvel",
      author_email="franck.chauvel@sintef.no",
      url="https://github.com/STAMP-project/ozepy",
      py_modules=["greetings"],
      install_requires = [
          "flask == 1.0.2"
      ]
)
