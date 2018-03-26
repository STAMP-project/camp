
from setuptools import setup, find_packages

# Replace the place holders with values for your project

setup(

    name='camp-realize',

    version='0.1',
    author='SINTEF Digital',
    author_email='anatoly.vasilevskiy@sintef.no',
    description='realization module for camp',

    # This must correspond to the actual packages in the plugin.
    packages=find_packages(exclude=['tests']),

    license='MIT LICENSE',
    zip_safe=False,
    install_requires=['pyyaml'],
    entry_points={  # Optional
        'console_scripts': [
            'rcamp=camp_real_engine.rcamp:rcamp_main',
        ],
    }
)
