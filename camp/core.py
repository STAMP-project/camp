#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.directories import InputDirectory, OutputDirectory
from camp.execute.parsers import ConfigINIParser
from camp.execute.command.commands import ConductExperimentRunner



class Camp(object):


    def __init__(self, codec, solver, realize):
        self._codec = codec
        self._problem = solver
        self._builder = realize
        self._input = None
        self._output = None


    def generate(self, arguments):
        self._prepare_directories(arguments)
        model = self._load_model()
        configurations = self._generate_configurations(arguments, model)
        for index, each_configuration in enumerate(configurations, 1):
            self._save(index, each_configuration)


    def _prepare_directories(self, arguments):
        self._input = InputDirectory(arguments.working_directory,
                                               self._codec)
        self._output = OutputDirectory(arguments.working_directory + "/out",
                                               self._codec)


    def _load_model(self):
        file_name, model, warnings = self._input.model
        print "Model loaded from '%s'." % file_name
        for each_warning in warnings:
            print " - WARNING: ", str(each_warning)
        return model


    def _generate_configurations(self, arguments, model):
        print "Searching for configurations ..."
        problem = self._problem.from_model(model)
        if arguments.only_coverage:
            return  problem.coverage()
        return problem.all_solutions()


    def _save(self, index, configuration):
        self._output.save_as_graphviz(index, configuration)
        yaml_file = self._output.save_as_yaml(index, configuration)
        print("\n - Config. %d in '%s'." % (index, yaml_file))
        self._summarize(configuration)


    def _summarize(self, configuration):
        components = set()
        for each in configuration.instances:
            name = each.definition.name
            if each.configuration:
                name  += " (" +", ".join(str(v) for _,v in each.configuration) + ")"
            components.add(name)
        text = "   Includes " + ', '.join(components)
        if len(text) > 75:
            text = text[:75] + " ... "
        print text


    def realize(self, arguments):
        self._prepare_directories(arguments)
        model = self._load_model()
        for path, each_configuration in self._load_configurations(model):
            print " - Building '%s' ..." % path
            self._builder.build(each_configuration,
                                arguments.working_directory,
                                path)


    def _load_configurations(self, model):
        print "Searching configurations in '%s' ..." % self._output._path
        return self._output.existing_configurations(model)


    def execute(self, arguments):
        parser = ConfigINIParser()
        config = parser.parse(arguments.configuration_file)
        experiment = ConductExperimentRunner(config)
        result = experiment.run()
