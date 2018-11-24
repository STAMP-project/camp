#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp import About



class UI(object):
    """
    Print CAMP events on the terminal or on any other given output
    """

    def __init__(self, output=None):
        from sys import stdout
        self._output = output or stdout


    def welcome(self):
        self._print("{program} v{version} ({ipr})",
                    program=About.PROGRAM,
                    version=About.VERSION,
                    ipr=About.LICENSE)
        self._print(About.COPYRIGHT)
        self._print("")


    def goodbye(self):
        self._print("\nThat's all folks!")


    def model_loaded(self, path, model):
        self._print("Loaded '{path}'.", path=path)


    def new_configuration(self, index, configuration, path):
        self._print("\n - Config. {index} in '{path}'.",
                    index=index,
                    path=path)
        self._summarize(configuration)


    def configurations_loaded(self, path):
        self._print("Loading configurations from '{path}' ...", path=path)


    def configuration_realized(self, path):
        self._print(" - Built configuration '{path}.", path=path)


    def warns(self, warnings):
        if warnings:
            self._print("Warnings ...")
            for each in warnings:
                self._print(" - {warning}", warning=str(each))

    def invalid_yaml_model(self, error):
        self._print("\nError:")
        self._print(" - There are errors in the CAMP YAML model.")
        self._print("   Please fix the following issue before to proceed:")
        for index, each_warning in enumerate(error.warnings, 1):
            self._print(" {index}. {warning}", index=index, warning=str(each))


    def missing_model(self, error):
        self._print("\nError:")
        self._print(" - Unable to find a CAMP model in '{folder}'.",
                    folder=error.searched_folder)
        file_names = ", ".join(error.searched_files)
        self._print("   CAMP looks for one of the following: {file_names}.",
                    file_names=file_names)


    def no_configuration_found(self, error):
        self._print("\nError:")
        self._print(" - Unable to find any generated configuration  in '{folder}'.",
                    folder=error.searched_folder)
        self._print("   Have you run 'camp generate -d {folder}?",
                    folder=error.searched_folder)


    def unexpected_error(self, error):
        self._print("Unexpected error:")
        self._print(" - " + str(error))
        self._print("   Please report this at '{issue}'.",
                    issue=self.ISSUE_PAGE)

    ISSUE_PAGE = "https://github.com/STAMP-project/camp/issues"


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
        self._print(text)


    def _print(self, pattern, **values):
        if values:
            self._output.write(pattern.format(**values) + "\n")
        else:
            self._output.write(pattern+ "\n")
