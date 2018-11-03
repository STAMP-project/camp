#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from camp.codecs.yaml import YAML
from camp.core import Camp
from camp.generate import Z3Problem
from camp.realize import Builder
from camp.run import Runner


from os import listdir
from os.path import join, isdir, exists

from re import match

from shutil import rmtree, copytree

from unittest import TestCase



class FilesAreGenerated(TestCase):


    def test_single_component(self):
        self.prepare_sample("single_component")
        
        self.invoke_camp_generate()
        
        self.assert_configuration_count_is(1)


    def test_variables(self):
        self.prepare_sample("variables")
        
        self.invoke_camp_generate()

        self.assert_configuration_count_is(3)


    def test_stack(self):
        self.prepare_sample("stack")
        
        self.invoke_camp_generate()
        
        self.assert_configuration_count_is(2)


    def test_orchestrations(self):
        self.prepare_sample("orchestrations")
        
        self.invoke_camp_generate()
        
        self.assert_configuration_count_is(2)
        
        
    def prepare_sample(self, sample_name):
        sample_directory = join(self.SAMPLES_DIRECTORY, sample_name)
        self._working_directory = join(self.WORKING_DIRECTORY, sample_name)
        if isdir(self._working_directory):
            rmtree(self._working_directory)
        copytree(sample_directory, self._working_directory)


    WORKING_DIRECTORY = "temp"
    SAMPLES_DIRECTORY = "samples"


    def invoke_camp_generate(self):
        runner = Runner(Camp(YAML(),
                             Z3Problem,
                             Builder()))
        runner.start(["generate", "--all", "-d", self._working_directory])


    def assert_configuration_count_is(self, expected):
        generated = []
        for each_file in listdir(self._working_directory):
            if match(r"config_\d+", each_file):
                generated.append(each_file)
        self.assertEqual(expected, len(generated), str(generated))
                     
        
        
    def verify_generated_files(self, *expected_files):
        for each in expected_files:
            path = join(self._working_directory, each)
            self.assertTrue(exists(path),
                            "Expecting file '%s', but could not find it!" % path)

