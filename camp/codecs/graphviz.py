#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from camp.codecs.commons import Codec



class Graphviz(Codec):


    def __init__(self, indentation=2):
        self._indentation_level = 0
        self._indentation_width = indentation
        self._stream = None



    def save_configuration(self, configuration, stream):
        self._stream = stream
        self._write("digraph Config {")
        self._indent()
        self._declare_nodes_options()

        for index, each_stack in enumerate(configuration.stacks, 1):
            self._declare_cluster(each_stack, index)

        for any_instance in configuration.instances:
            if any_instance.service_providers:
                for each_provider in any_instance.service_providers:
                    self._declare_egde(any_instance, each_provider)

        self._dedent()
        self._write("}")


    def _write(self, text):
        if not self._stream:
            raise AssertionError("Cannot write, no stream is defined.")

        self._stream.write(" " * self._indentation_level * self._indentation_width)
        self._stream.write(text)
        self._stream.write("\n")


    def _indent(self):
        self._indentation_level += 1


    def _declare_nodes_options(self):
        self._write("node [shape=\"record\","
                    "style=\"filled\","
                    "fillcolor=\"white\"];")


    def _declare_cluster(self, stack, index):
        self._write("subgraph cluster_%d {" % index)
        self._indent()
        self._declare_container_options(index)

        for each_instance in stack:
            self._declare_node(each_instance)

        for each_instance in stack:
            if each_instance.feature_provider:
                self._declare_egde(each_instance, each_instance.feature_provider)

        self._dedent()
        self._write("}")


    def _declare_container_options(self, index):
        self._write("label=\"container %d\";" % index)
        self._write("style=\"filled\";")
        self._write("color=\"lightgrey\";")


    def _declare_node(self, instance):
        if instance.configuration:
            options = "\l".join(["%s=%s" % (k.name,v) for k,v in instance.configuration])
            self._write(
                "%s [label=\"{%s|%s}\"];" % (
                    self._escape(instance.name),
                    instance.definition.name,
                    options))
        else:
            self._write(
                "%s [label=\"%s\"];" % (
                    self._escape(instance.name),
                    instance.definition.name))


    def _declare_egde(self, source, target):
        self._write("%s -> %s;" % (self._escape(source.name),
                                   self._escape(target.name)))


    def _dedent(self):
        if self._indentation_level == 0:
            raise AssertionError("Invalid dedent operation!")
        self._indentation_level -= 1



    @staticmethod
    def _escape(text):
        return text.replace("-", "_")
