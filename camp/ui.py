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


    def error(self, error):
        if hasattr(error, "problem"):
            self._print("\nError:")
            self._print("  - {problem}", problem=error.problem)
            self._print("    {hint}", hint=error.hint)
        else:
            self._print(str(error))


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
