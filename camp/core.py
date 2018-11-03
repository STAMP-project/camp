#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from camp.codecs.graphviz import Graphviz
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
        self._arguments = None


    def generate(self, arguments):
        self._arguments = arguments
        model = self._load_model()

        problem = self._problem.from_model(model)

        if arguments.only_coverage:
            configurations = problem.coverage()
        else:
            configurations = problem.all_solutions()
            
        print configurations.__name__
        print "Searching for configurations ..."        
        for index, each_configuration in enumerate(configurations, 1):
            self._save_as_yaml(index, each_configuration)
            self._save_as_graphviz(index, each_configuration)
            self._summarize(each_configuration)
        print("No more configurations.")

        

    def _load_model(self):
        path = join_paths(self._arguments.working_directory, "model.yml")
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


    def _save_as_yaml(self, index, configuration):
        directory = self._prepare_directory(index)
        destination = join_paths(directory, self.YAML_CONFIGURATION)
        with open(destination, "w") as stream:
            self._codec.save_configuration(configuration, stream)
        print("\n - Config. %d in '%s'." % (index, destination))

    YAML_CONFIGURATION = "configuration.yml"


    def _prepare_directory(self, index):
        directory = join_paths(self._arguments.working_directory, "config_%d" % index)
        if not isdir(directory):
            mkdir(directory)
        return directory


    def _save_as_graphviz(self, index, configuration):
        directory = self._prepare_directory(index)
        destination = join_paths(directory, "configuration.dot")
        with open(destination, "w") as stream:
            graphviz = Graphviz()
            graphviz.save_configuration(configuration, stream)
 

    def realize(self, arguments):
        self._arguments = arguments
        model = self._load_model()
        for location, each_configuration in self._load_configurations(model, arguments):
            self._builder.build(each_configuration,
                                arguments.working_directory,
                                location)


    def _load_configurations(self, model, arguments):
        print "Searching configurations in '%s' ..." % arguments.output_directory
        for each_file in listdir(arguments.output_directory):
            path = join_paths(arguments.output_directory, each_file)
            if match(r"^config_[0-9]+$", each_file) \
               and isdir(path):
                location = join_paths(path, self.YAML_CONFIGURATION)
                print " - Loading '%s' ..." % location
                with open(location, "r") as stream:
                    configuration = self._codec.load_configuration_from(model, stream)
                    yield path, configuration
                    

    def execute(self, arguments):
        parser = ConfigINIParser()
        config = parser.parse(arguments.configuration_file)
        experiment = ConductExperimentRunner(config)
        result = experiment.run()
