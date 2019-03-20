#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.yaml import InvalidYAMLModel
from camp.directories import InputDirectory, OutputDirectory, \
    MissingModel, NoConfigurationFound
from camp.entities.validation import Checker, InvalidModel
from camp.execute.commons import SimulatedShell, Shell, ShellCommandFailed
from camp.execute.select import select_executor, TechnologyNotSupported
from camp.ui import UI

from traceback import extract_tb

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

        except InvalidYAMLModel as error:
            self._ui.invalid_yaml_model(error)

        except InvalidModel as error:
            self._ui.invalid_model(error)

        except MissingModel as error:
            self._ui.missing_model(error)

        except Exception as error:
            stack_trace = extract_tb(exc_info()[2])
            self._ui.unexpected_error(error, stack_trace)

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
        model.accept(Checker(workspace=self._input.path))
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

        except InvalidYAMLModel as error:
            self._ui.invalid_yaml_model(error)

        except InvalidModel as error:
            self._ui.invalid_model(error)

        except MissingModel as error:
            self._ui.missing_model(error)

        except NoConfigurationFound as error:
            self._ui.no_configuration_found(error)

        except Exception as error:
            stack_trace = extract_tb(exc_info()[2])
            self._ui.unexpected_error(error, stack_trace)

        finally:
            self._ui.goodbye()


    def _load_configurations(self, model):
        configurations = self._output.existing_configurations(model)
        self._ui.configurations_loaded(self._output.path)
        return configurations


    def execute(self, arguments):
        self._ui.welcome()
        self._prepare_directories(arguments)
        try:
            model = self._load_model()
            configurations = self._load_configurations(model)
            with open("camp_execute.log", "w") as log_file:
                shell = SimulatedShell(log_file, ".") if arguments.is_simulated \
                        else Shell(log_file, ".")
                execute = select_executor(arguments.testing_tool, shell)
                reports = execute(configurations, arguments.component)
                self._output.save_reports(reports)
                self._ui.summarize_execution(reports)


        except InvalidYAMLModel as error:
            self._ui.invalid_yaml_model(error)

        except InvalidModel as error:
            self._ui.invalid_model(error)

        except MissingModel as error:
            self._ui.missing_model(error)

        except NoConfigurationFound as error:
            self._ui.no_configuration_found(error)

        except ShellCommandFailed as error:
            self._ui.shell_command_failed(error)

        except TechnologyNotSupported as error:
            self._ui.technology_not_supported(error)

        except Exception as error:
            stack_trace = extract_tb(exc_info()[2])
            self._ui.unexpected_error(error, stack_trace)

        finally:
            self._ui.goodbye()
