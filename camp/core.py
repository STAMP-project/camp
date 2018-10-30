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

from os import mkdir
from os.path import join



class Camp(object):


    def __init__(self, codec, solver, realize):
        self._codec = codec
        self._problem = solver


    def generate(self, arguments):
        model = self._load_model(arguments)
                
        problem = self._problem.from_model(model)
        print "Searching for alternative configurations ..."
        for index, each_configuration in enumerate(problem.all_solutions(), 1):
            directory = join(arguments.working_directory, "config_%d" % index)
            mkdir(directory)
            destination = join(directory, "configuration.yml")
            print(" - Config. %d in '%s'." % (index, destination))
            self._summarize(each_configuration)

            with open(destination, "w") as stream:

                self._codec.save_configuration(each_configuration, stream)

        print("No more configurations.")


    def _load_model(self, arguments):
        path = join(arguments.working_directory, "model.yml")
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
	products = self._realize.get_products(arguments.products_file)
	for each_product in products:
	    self._realize.realize_product(each_product)

            
    def execute(self, arguments):
        parser = ConfigINIParser()
	config = parser.parse(arguments.configuration_file)
	experiment = ConductExperimentRunner(config)
	result = experiment.run()
