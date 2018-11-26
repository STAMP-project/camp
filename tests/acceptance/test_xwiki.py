#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from tests.acceptance.commons import CampTests, Sample

from unittest import skip



class FilesAreGenerated(CampTests):


    def setUp(self):
        self.sample = Sample("stamp/xwiki", self.WORKSPACE)


    WORKSPACE = "tmp/acceptance"


    @skip("Take too long, about 45 min.")
    def test_after_we_generate_all(self):
        self.generate_all()
        self.assertEqual(64, len(self.sample.generated_configurations))

    @skip("Take too long")
    def test_after_we_generate_coverage(self):
        self.generate_coverage()
        self.assertEqual(4, len(self.sample.generated_configurations))


    def test_after_we_realize_coverage(self):
        self.create_configurations(self.CONFIG_1)

        self.realize()

        self.assertEqual(1, len(self.sample.generated_configurations))

        configuration = self.sample.generated_configurations[0]

        self._assert_generated(configuration,
                               "docker-compose.yml",
                               "images/build_images.sh",
                               "images/tomcat8_0/Dockerfile",
                               "images/xwiki8postgres_0/Dockerfile",
                               "images/xwiki8postgres_0/tomcat/setenv.sh",
                               "images/xwiki8postgres_0/xwiki/docker-entrypoint.sh",
                               "images/xwiki8postgres_0/xwiki/hibernate.cfg.xml")


    CONFIG_1 = ("instances:\n"
                "  openjdk8_0:\n"
                "    configuration: {}\n"
                "    definition: openjdk8\n"
                "    service_providers: []\n"
                "  postgres9_0:\n"
                "    configuration: {}\n"
                "    definition: postgres9\n"
                "    service_providers: []\n"
                "  tomcat8_0:\n"
                "    configuration: {}\n"
                "    definition: tomcat8\n"
                "    feature_provider: openjdk8_0\n"
                "    service_providers: []\n"
                "  xwiki8postgres_0:\n"
                "    configuration: {}\n"
                "    definition: xwiki8postgres\n"
                "    feature_provider: tomcat8_0\n"
                "    service_providers:\n"
                "    - postgres9_0\n")
