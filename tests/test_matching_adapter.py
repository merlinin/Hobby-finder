import unittest

from matching.adapter import MatchingAdapter


class MatchingAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.adapter = MatchingAdapter()
        self.canonical_names = ["Klettern", "Programmieren", "Radfahren", "Gitarre spielen"]

    def test_exact_name_match_is_detected(self):
        result = self.adapter.match_activity("Klettern", self.canonical_names)

        self.assertTrue(result.matched)
        self.assertEqual(result.activity_name, "Klettern")
        self.assertEqual(result.match_type, "exact_name")
        self.assertEqual(result.confidence, 1.0)

    def test_alias_match_is_detected(self):
        result = self.adapter.match_activity("bouldern", self.canonical_names)

        self.assertTrue(result.matched)
        self.assertEqual(result.activity_name, "Klettern")
        self.assertEqual(result.match_type, "exact_alias")


    def test_additional_aliases_are_detected(self):
        mountainbike = self.adapter.match_activity("mountainbike", self.canonical_names)
        gitarre = self.adapter.match_activity("gitarre", self.canonical_names)

        self.assertTrue(mountainbike.matched)
        self.assertEqual(mountainbike.activity_name, "Radfahren")
        self.assertEqual(mountainbike.match_type, "exact_alias")

        self.assertTrue(gitarre.matched)
        self.assertEqual(gitarre.activity_name, "Gitarre spielen")

    def test_case_and_whitespace_normalization_is_applied(self):
        result = self.adapter.match_activity("  kLeTtErN ", self.canonical_names)

        self.assertTrue(result.matched)
        self.assertEqual(result.activity_name, "Klettern")

    def test_unknown_activity_returns_no_match(self):
        result = self.adapter.match_activity("stricken", self.canonical_names)

        self.assertFalse(result.matched)
        self.assertEqual(result.match_type, "none")
        self.assertEqual(result.confidence, 0.0)


if __name__ == "__main__":
    unittest.main()
