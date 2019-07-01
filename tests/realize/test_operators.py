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



class ComponentResourceSelectionShould(CampTest):


    def setUp(self):
        self.scenario = Scenario()

    def test_handle_files(self):
        self.scenario.create_template("nginx", "Dockerfile")
        self.scenario.create_template(None, "nginx_docker-compose.yml")
        self.scenario.create_template(None, "apache_docker-compose.yml")

        self.scenario.create_model(
            "goals:\n"
            "  running: [ MyService ]\n"
            "components:\n"
            "  nginx:\n"
            "    provides_services: [ MyService ]\n"
            "    realization:\n"
            "      - select: nginx_docker-compose.yml\n"
            "        instead_of:\n"
            "          - apache_docker-compose.yml\n"
            "        as: docker-compose.yml\n"
            "    implementation:\n"
            "      docker:\n"
            "        file: nginx/Dockerfile\n"
        )

        self.generate_all()
        self.realize()

        configurations = self.scenario.generated_configurations
        for each_configuration in self.scenario.generated_configurations:
            self._assert_generated(each_configuration, "docker-compose.yml")

        for each_configuration in self.scenario.generated_configurations:
            self._assert_missing(each_configuration,
                                 "nginx_docker-compose.yml",
                                 "apache_docker-compose.yml")


    def test_select_resource_before_substitutions_take_place(self):
        self.scenario.create_template("nginx", "Dockerfile")
        self.scenario.create_template(None,
                                      "nginx_docker-compose.yml",
                                      "build: ./nginx\n"
                                      "nginx_variable=value")
        self.scenario.create_template(None,
                                      "apache_docker-compose.yml",
                                      "apache_variable=value")

        self.scenario.create_model(
            "goals:\n"
            "  running: [ MyService ]\n"
            "components:\n"
            "  nginx:\n"
            "    provides_services: [ MyService ]\n"
            "    variables:\n"
            "      version:\n"
            "        values: [ v2.0 ]\n"
            "        realization:\n"
            "          - targets: [docker-compose.yml]\n"
            "            pattern: nginx_variable=value\n"
            "            replacements:\n"
            "             - nginx_variable=something_else\n"
            "    realization:\n"
            "      - select: nginx_docker-compose.yml\n"
            "        instead_of:\n"
            "          - apache_docker-compose.yml\n"
            "        as: docker-compose.yml\n"
            "    implementation:\n"
            "      docker:\n"
            "        file: nginx/Dockerfile\n"
        )

        self.generate_all()
        self.realize()

        configurations = self.scenario.generated_configurations
        self.assertEquals(1, len(configurations))
        for each_configuration in self.scenario.generated_configurations:
            self._assert_generated(each_configuration, "docker-compose.yml")

            self.assertIn("nginx_variable=something_else",
                          each_configuration.content_of("docker-compose.yml"))
            self.assertIn("build: ./images/nginx_0",
                          each_configuration.content_of("docker-compose.yml"))
