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
from camp.execute.engine import Engine, SimulatedShell, Shell, \
    ServiceNotReady, ShellCommandFailed, ReportFormatNotSupported
from camp.realize import InvalidSubstitution
from camp.ui import UI

from platform import system, dist, release

from subprocess import check_output

from traceback import extract_tb

from sys import exc_info, version_info



class Camp(object):


    def __init__(self, codec, solver, realize):
        self._codec = codec
        self._problem = solver
        self._builder = realize
        self._input = None
        self._output = None
        self._ui = UI()


    def show_versions(self):
        self._ui.welcome()

        os_version = system() + " " + release() + " (" + " ".join(dist()).strip() +")"

        python = version_info

        import z3;
        z3_version = z3.get_version_string()

        docker_version = check_output(["docker", "--version"]).decode("utf-8")
        compose_version = check_output(["docker-compose", "--version"]).decode("utf-8")

        self._ui.show_versions(os_version,
                               python,
                               z3_version,
                               docker_version.strip(),
                               compose_version.strip())

    def generate(self, arguments):
        self._ui.welcome()
        self._prepare_directories(arguments)
        try:
            model = self._load_model()
            configurations = self._generate_configurations(arguments, model)

            count = 0
            for index, each_configuration in enumerate(configurations, 1):
                self._save(index, each_configuration)
                count += 1

            if count == 0:
                self._ui.no_configuration_generated()


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
        path, model, _ = self._input.model
        self._ui.model_loaded(path, model)
        model.accept(Checker(workspace=self._input.path))
        return model


    def _generate_configurations(self, arguments, model):
        problem = self._problem.from_model(model)
        if arguments.only_coverage:
            return  problem.coverage()
        return problem.all_solutions()


    def _save(self, index, configuration):
        yaml_file = self._output.save_as_yaml(index, configuration)
        self._output.save_as_graphviz(index, configuration)
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

        except InvalidSubstitution as error:
            self._ui.invalid_substitution(error)

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
            testing = model.tests
            configurations = self._load_configurations(model)
            selected_configurations = self._filter(arguments, list(configurations))
            with open("camp_execute.log", "wb") as log_file:
                shell = self._select_shell(arguments, log_file)
                engine = Engine(testing,
                                shell,
                                self._ui,
                                arguments.retry_count,
                                arguments.retry_delay)
                reports = engine.execute(selected_configurations)
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

        except ServiceNotReady as error:
            self._ui.service_not_ready(error)

        except ReportFormatNotSupported as error:
            self._ui.report_format_not_supported(error)

        except Exception as error:
            stack_trace = extract_tb(exc_info()[2])
            self._ui.unexpected_error(error, stack_trace)

        finally:
            self._ui.goodbye()


    def _select_shell(self, arguments, log_file):
        shell = Shell(log_file, ".", self._ui)
        if arguments.is_simulated:
            shell = SimulatedShell(log_file, ".", self._ui)
        return shell


    def _filter(self, arguments, configurations):
        if len(arguments._included) == 0:
            return configurations

        selection = []
        for each_index in arguments._included:
            found = self._search_for(each_index, configurations)
            if not found:
                self._ui.no_configuration_with_index(each_index)
            else:
                selection.append(found)
        return selection


    def _search_for(self, index, configurations):
        marker = "config_{}".format(index)
        for any_path, any_config in configurations:
            if marker in any_path:
                return (any_path, any_config)
        return None
