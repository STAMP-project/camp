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
from camp.entities.validation import Checker
from camp.errors import MissingModel, NoConfigurationFound
from camp.execute.parsers import ConfigINIParser
from camp.execute.command.commands import ConductExperimentRunner
from camp.ui import UI

from sys import exc_info


class Camp(object):


    def __init__(self, codec, solver, realize):
        self._codec = codec
        self._problem = solver
        self._builder = realize
        self._input = None
        self._output = None
        self._ui = UI()


    def generate(self, arguments):
        self._ui.welcome()
        self._prepare_directories(arguments)
        try:
            model = self._load_model()
            configurations = self._generate_configurations(arguments, model)
            for index, each_configuration in enumerate(configurations, 1):
                self._save(index, each_configuration)

        except MissingModel as error:
            self._ui.missing_model(error)

        except Exception as error:
            self._ui.unexpected_error(error)

        finally:
            self._ui.goodbye()


    def _prepare_directories(self, arguments):
        self._input = InputDirectory(arguments.working_directory,
                                               self._codec)
        self._output = OutputDirectory(arguments.working_directory + "/out",
                                               self._codec)


    def _load_model(self):
        path, model, warnings = self._input.model
        self._ui.model_loaded(path, model)
        self._ui.warns(warnings)

        checker = Checker(workspace=self._input.path)
        model.accept(checker)
        self._ui.warns(checker.errors)

        return model


    def _generate_configurations(self, arguments, model):
        problem = self._problem.from_model(model)
        if arguments.only_coverage:
            return  problem.coverage()
        return problem.all_solutions()


    def _save(self, index, configuration):
        self._output.save_as_graphviz(index, configuration)
        yaml_file = self._output.save_as_yaml(index, configuration)
        self._ui.new_configuration(index, configuration, yaml_file)


    def realize(self, arguments):
        self._ui.welcome()
        self._prepare_directories(arguments)
        try:
            model = self._load_model()
            for path, each_configuration in self._load_configurations(model):
                self._builder.build(each_configuration,
                                    arguments.working_directory,
                                    path)
                self._ui.configuration_realized(path)

        except MissingModel as error:
            self._ui.missing_model(error)

        except NoConfigurationFound as error:
            self._ui.no_configuration_found(error)

        except Exception as error:
            self._ui.unexpected_error(error)

        finally:
            self._ui.goodbye()


    def _load_configurations(self, model):
        configurations = self._output.existing_configurations(model)
        self._ui.configurations_loaded(self._output.path)
        return configurations


    @staticmethod
    def execute(self, arguments):
        self._ui.welcome()
        try:
            parser = ConfigINIParser()
            config = parser.parse(arguments.configuration_file)
            experiment = ConductExperimentRunner(config)
            experiment.run()

        except:
            self._ui.error(sys.exc_info()[0])

        finally:
            self._ui.goodbye()
