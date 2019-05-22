#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from tests.commons import Scenario, CampTest



class ResourceSelectionShould(CampTest):


    def setUp(self):
        self.scenario = Scenario()


    def test_handle_files(self):
        self.scenario.create_template("server", "Dockerfile")
        self.scenario.create_template("server", "nginx_settings.py")
        self.scenario.create_template("server", "apache_settings.py")

        self.scenario.create_model(
            "goals:\n"
            "  running: [ MyService ]\n"
            "components:\n"
            "  server:\n"
            "    provides_services: [ MyService ]\n"
            "    variables:\n"
            "      proxy:\n"
            "        values: [ nginx, apache ]\n"
            "        realization:\n"
            "         - select: \n"
            "             - server/nginx_settings.py\n"
            "             - server/apache_settings.py\n"
            "           as: server/settings.py\n"
            "    implementation:\n"
            "      docker:\n"
            "        file: server/Dockerfile\n"
        )

        self.generate_all()
        self.realize()

        configurations = self.scenario.generated_configurations
        for each_configuration in self.scenario.generated_configurations:
            self._assert_generated(each_configuration, "images/server_0/settings.py")


    def test_handle_selecting_without_renaming(self):
        self.scenario.create_template("server", "Dockerfile")
        self.scenario.create_template("server", "nginx_settings.py")
        self.scenario.create_template("server", "apache_settings.py")

        self.scenario.create_model(
            "goals:\n"
            "  running: [ MyService ]\n"
            "components:\n"
            "  server:\n"
            "    provides_services: [ MyService ]\n"
            "    variables:\n"
            "      proxy:\n"
            "        values: [ nginx, apache ]\n"
            "        realization:\n"
            "         - select: \n"
            "             - server/nginx_settings.py\n"
            "             - server/apache_settings.py\n"
            "    implementation:\n"
            "      docker:\n"
            "        file: server/Dockerfile\n"
        )

        self.generate_all()
        self.realize()

        configurations = self.scenario.generated_configurations
        for each_configuration in self.scenario.generated_configurations:
            if each_configuration.model.resolve("server_0")["proxy"] == "nginx":
                self._assert_generated(each_configuration,
                                       "images/server_0/nginx_settings.py")
            elif each_configuration.model.resolve("server_0")["proxy"] == "apache":
                self._assert_generated(each_configuration,
                                       "images/server_0/apache_settings.py")



    def test_handle_directory(self):
        self.scenario.create_template("server", "Dockerfile")
        self.scenario.create_template("server", "nginx/settings.py")
        self.scenario.create_template("server", "apache/settings.py")

        self.scenario.create_model(
            "goals:\n"
            "  running: [ MyService ]\n"
            "components:\n"
            "  server:\n"
            "    provides_services: [ MyService ]\n"
            "    variables:\n"
            "      proxy:\n"
            "        values: [ nginx, apache ]\n"
            "        realization:\n"
            "         - select: \n"
            "             - server/nginx\n"
            "             - server/apache\n"
            "           as: server/config\n"
            "    implementation:\n"
            "      docker:\n"
            "        file: server/Dockerfile\n"
        )

        self.generate_all()
        self.realize()

        configurations = self.scenario.generated_configurations
        for each_configuration in self.scenario.generated_configurations:
            self._assert_generated(each_configuration, "images/server_0/config")
