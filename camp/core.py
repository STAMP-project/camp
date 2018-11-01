#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.execute.parsers import ConfigINIParser
from camp.execute.command.commands import ConductExperimentRunner

from os import mkdir, listdir
from os.path import isdir, join as join_paths

from re import match



class Camp(object):


    def __init__(self, codec, solver, realize):
        self._codec = codec
        self._problem = solver
        self._builder = realize


    def generate(self, arguments):
        model = self._load_model(arguments)

        problem = self._problem.from_model(model)
        print "Searching for alternative configurations ..."
        for index, each_configuration in enumerate(problem.all_solutions(), 1):
            directory = join_paths(arguments.working_directory, "config_%d" % index)
            mkdir(directory)
            destination = join_paths(directory, "configuration.yml")
            print(" - Config. %d in '%s'." % (index, destination))
            self._summarize(each_configuration)

            with open(destination, "w") as stream:

                self._codec.save_configuration(each_configuration, stream)

        print("No more configurations.")


    def _load_model(self, arguments):
        path = join_paths(arguments.working_directory, "model.yml")
        print("Loading model from '%s' ... " % path)
        with open(path, "r") as stream:
            model = self._codec.load_model_from(stream)
            for each_warning in self._codec.warnings:
                print " - WARNING: ", str(each_warning)
            return model


    def _summarize(self, configuration):
        components = set()
        for each in configuration.instances:
            name = each.definition.name
            if each.configuration:
                name  += " (" +", ".join(v for _,v in each.configuration) + ")"
            components.add(name)
        text = "   Includes " + ', '.join(components)
        if len(text) > 75:
            text = text[:75] + " ... "
        print text


    def realize(self, arguments):
        model = self._load_model(arguments)
        for location, each_configuration in self._load_configurations(model, arguments):
            self._builder.build(each_configuration,
                                arguments.working_directory,
                                location)


    def _load_configurations(self, model, arguments):
        print "Searching configuration in '%s' ..." % arguments.output_directory
        for each_file in listdir(arguments.output_directory):
            path = join_paths(arguments.output_directory, each_file)
            if match(r"^config_[0-9]+$", each_file) \
               and isdir(path):
                location = join_paths(path, "configuration.yml")
                print " - Loading '%s' ..." % location
                with open(location, "r") as stream:
                    configuration = self._codec.load_configuration_from(model, stream)
                    yield path, configuration


    def execute(self, arguments):
        parser = ConfigINIParser()
        config = parser.parse(arguments.configuration_file)
        experiment = ConductExperimentRunner(config)
        result = experiment.run()
