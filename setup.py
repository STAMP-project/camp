
from setuptools import setup

# Replace the place holders with values for your project

setup(

    name='camp-realize',

    version='0.1',
    author='SINTEF Digital',
    author_email='anatoly.vasilevskiy@sintef.no',
    description='realization module for camp',

    # This must correspond to the actual packages in the plugin.
    packages=['camp_real_engine'],

    license='LICENSE',
    zip_safe=False,
    test_requires=[
        "nose"
        "mock>=2.0.0"
    ]
)
