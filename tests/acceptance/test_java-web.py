from tests.commons import CampTest, Scenario

class JavaWebTestManShould(CampTest):


    def setUp(self):
        self.scenario = Scenario.from_sample("java-web")


    def test_yield_three_configurations(self):
        self.generate_all()

        configurations = self.scenario.generated_configurations

        self.assertEqual(3, len(configurations))


    def test_run_all_tests_three_times(self):
        self.generate_all()
        self.realize()
        self.execute()

        report = self.scenario.fetch_test_report()

        self.assertEqual(3, len(report["reports"]))
