import unittest
from root_cause_analyzer import get_analyzer

class TestRootCauseAnalyzer(unittest.TestCase):
    def test_algorithm_a(self):
        analyzer = get_analyzer('A')
        result = analyzer.analyze(data={})
        self.assertEqual(result, "Result from Adtributor")

    def test_algorithm_b(self):
        analyzer = get_analyzer('B')
        result = analyzer.analyze(data={})
        self.assertEqual(result, "Result from RecursiveAdtributor")

if __name__ == '__main__':
    unittest.main()
