#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from tests.acceptance.commons import CampTests, Sample



class FilesAreGenerated(CampTests):


    def setUp(self):
        self.sample = Sample("stamp/atos")


    def test_generate_coverage(self):
        self.generate_coverage()
        self.assertEqual(10, len(self.sample.generated_configurations))



    def test_after_we_realize_coverage(self):
        self.create_configurations(self.CONFIG_1, self.CONFIG_2)

        self.realize()

        self.assertEqual(2, len(self.sample.generated_configurations))

        configuration = self.sample.generated_configurations[0]

        self._assert_generated(configuration,
                               "docker-compose.yml",
                               "images/build_images.sh",
                               "images/postgres_0/Dockerfile",
                               "images/postgres_0/postgresql-template.conf",
                               "images/showcase_0/Dockerfile",
                               "images/showcase_0/mpm_prefork-template.conf",
                               "images/showcase_0/mpm_worker-template.conf")


    CONFIG_1 = ("instances:\n"
                "  postgres_0:\n"
                "    configuration: {}\n"
                "    definition: postgres\n"
                "    feature_provider: ubuntu_0\n"
                "    service_providers: []\n"
                "  python_0:\n"
                "    configuration: {}\n"
                "    definition: python\n"
                "    service_providers: []\n"
                "  showcase_0:\n"
                "    configuration:\n"
                "      max_request_workers: 1664\n"
                "      thread_limit: 128\n"
                "      threads_per_child: 104\n"
                "    definition: showcase\n"
                "    feature_provider: python_0\n"
                "    service_providers:\n"
                "    - postgres_0\n"
                "  ubuntu_0:\n"
                "    configuration: {}\n"
                "    definition: ubuntu\n"
                "    service_providers: []\n")


    CONFIG_2 = ("instances:\n"
                "  postgres_0:\n"
                "    configuration: {}\n"
                "    definition: postgres\n"
                "    feature_provider: ubuntu_0\n"
                "    service_providers: []\n"
                "  python_0:\n"
                "    configuration: {}\n"
                "    definition: python\n"
                "    service_providers: []\n"
                "  showcase_0:\n"
                "    configuration:\n"
                "      max_request_workers: 1792\n"
                "      thread_limit: 128\n"
                "      threads_per_child: 112\n"
                "    definition: showcase\n"
                "    feature_provider: python_0\n"
                "    service_providers:\n"
                "    - postgres_0\n"
                "  ubuntu_0:\n"
                "    configuration: {}\n"
                "    definition: ubuntu\n"
                "    service_providers: []\n")
