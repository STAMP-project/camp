#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from mock import patch

from tests.acceptance.commons import Sample, CampTests



WORKSPACE = "tmp/acceptance/errors"



class MissingCAMPModelIsReported(CampTests):


    def setUp(self):
        self.sample = Sample("no_camp_model", WORKSPACE)


    def test_when_we_generate_all(self):
        self.generate_all()


    def test_when_we_realize_configurations(self):
        self.realize()



class MissingConfigurationsAreReported(CampTests):


    def setUp(self):
        self.sample = Sample("no_camp_config", WORKSPACE)
        self.sample.create_model("goals:\n"
                                 "  running: [ Awesome ]\n"
                                 "components:\n"
                                 "   server:\n"
                                 "      provides_services: [ Awesome ]\n"
                                 "      implementation:\n"
                                 "         docker:\n"
                                 "            file: server/Dockerfile\n")
        self.sample.create_template("server", "Dockerfile", "DOESN'T MATTER")


    def test_with_camp_realize(self):
        self.realize()



class UnexpectedErrorsAreCaught(CampTests):


    def setUp(self):
        self.sample = Sample("no_camp_config", WORKSPACE)
        self.sample.create_model("goals:\n"
                                 "  running: [ Awesome ]\n"
                                 "components:\n"
                                 "   server:\n"
                                 "      provides_services: [ Awesome ]\n"
                                 "      implementation:\n"
                                 "         docker:\n"
                                 "            file: server/Dockerfile\n")
        self.sample.create_template("server", "Dockerfile", "DOESN'T MATTER")
        self.sample.create_configuration(1,
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
