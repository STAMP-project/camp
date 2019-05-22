#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from mock import patch

from tests.commons import Scenario, CampTest




class MissingCAMPModelIsReported(CampTest):


    def setUp(self):
        self.scenario = Scenario("missing_camp_model")


    def test_when_we_generate_all(self):
        self.generate_all()


    def test_when_we_realize_configurations(self):
        self.realize()



class MissingConfigurationsAreReported(CampTest):


    def setUp(self):
        self.scenario = Scenario("missing_configurations")
        self.scenario.create_model("goals:\n"
                                 "  running: [ Awesome ]\n"
                                 "components:\n"
                                 "   server:\n"
                                 "      provides_services: [ Awesome ]\n"
                                 "      implementation:\n"
                                 "         docker:\n"
                                 "            file: server/Dockerfile\n")
        self.scenario.create_template("server", "Dockerfile", "DOESN'T MATTER")


    def test_with_camp_realize(self):
        self.realize()


class VainSubstitutionAreReported(CampTest):


    def setUp(self):
        self.scenario = Scenario("vain_substitutions")
        self.scenario.create_model("goals:\n"
                                 "  running: [ Awesome ]\n"
                                 "components:\n"
                                 "   server:\n"
                                 "      provides_services: [ Awesome ]\n"
                                 "      variables:\n"
                                 "         memory:\n"
                                 "           values: [ 1GB, 2GB ]\n"
                                 "           realization:\n"
                                 "            - targets: [ server/Dockerfile ]\n"
                                 "              pattern: not found\n"
                                 "              replacements: \n"
                                 "                - \"whatever 1\"\n"
                                 "                - \"whatever 2\"\n"
                                 "      implementation:\n"
                                 "         docker:\n"
                                 "            file: server/Dockerfile\n")
        self.scenario.create_template("server", "Dockerfile", "Blah blah blah!")


    def test_with_camp_realize(self):
        self.generate_all()
        self.realize()



class UnexpectedErrorsAreCaught(CampTest):


    def setUp(self):
        self.scenario = Scenario("unexpected_errors")
        self.scenario.create_model("goals:\n"
                                 "  running: [ Awesome ]\n"
                                 "components:\n"
                                 "   server:\n"
                                 "      provides_services: [ Awesome ]\n"
                                 "      implementation:\n"
                                 "         docker:\n"
                                 "            file: server/Dockerfile\n")
        self.scenario.create_template("server", "Dockerfile", "DOESN'T MATTER")
        self.scenario.create_configuration(1,
                                         "instances:\n"
                                         "  server_0:\n"
                                         "    definition: server\n"
                                         "    configuration: {}\n")


    @patch("camp.generate.Z3Problem.all_solutions")
    def test_with_generate_all_configurations(self, mock):
        mock.side_effect = RuntimeError("This was really unexpected!")
        self.generate_all()


    @patch("camp.realize.Builder.build")
    def test_with_realize_configurations(self, mock):
        mock.side_effect = RuntimeError("This was really unexpected!")
        self.realize()


    @patch("camp.execute.engine.Engine.execute")
    def test_with_execute_configurations(self, mock):
        mock.side_effect = RuntimeError("This was really unexpected!")
        self.execute()
