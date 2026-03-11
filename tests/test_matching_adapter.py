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
        self.assertEqual(result.match_type, "exact_match")
        self.assertEqual(result.normalized_input, "klettern")
        self.assertEqual(result.confidence, 1.0)

    def test_alias_match_is_detected(self):
        result = self.adapter.match_activity("bouldern", self.canonical_names)

        self.assertTrue(result.matched)
        self.assertEqual(result.activity_name, "Klettern")
        self.assertEqual(result.match_type, "alias_match")


    def test_additional_aliases_are_detected(self):
        mountainbike = self.adapter.match_activity("mountainbike", self.canonical_names)
        gitarre = self.adapter.match_activity("gitarre", self.canonical_names)

        self.assertTrue(mountainbike.matched)
        self.assertEqual(mountainbike.activity_name, "Radfahren")
        self.assertEqual(mountainbike.match_type, "alias_match")

        self.assertTrue(gitarre.matched)
        self.assertEqual(gitarre.activity_name, "Gitarre spielen")

    def test_case_and_whitespace_normalization_is_applied(self):
        result = self.adapter.match_activity("  kLeTtErN ", self.canonical_names)

        self.assertTrue(result.matched)
        self.assertEqual(result.activity_name, "Klettern")


    def test_hyphen_and_punctuation_variations_are_normalized(self):
        result = self.adapter.match_activity(" 3D-Druck! ", self.canonical_names + ["3D-Druck"])

        self.assertTrue(result.matched)
        self.assertEqual(result.activity_name, "3D-Druck")
        self.assertEqual(result.match_type, "exact_match")

    def test_simple_phrase_variants_are_simplified(self):
        canonical_names = self.canonical_names + ["Musik machen"]

        klettern = self.adapter.match_activity("klettern gehen", canonical_names)
        musik = self.adapter.match_activity("musik machen", canonical_names)
        fahrrad = self.adapter.match_activity("fahrrad fahren", canonical_names)

        self.assertTrue(klettern.matched)
        self.assertEqual(klettern.activity_name, "Klettern")
        self.assertEqual(klettern.match_type, "normalized_match")

        self.assertTrue(musik.matched)
        self.assertEqual(musik.activity_name, "Musik machen")

        self.assertTrue(fahrrad.matched)
        self.assertEqual(fahrrad.activity_name, "Radfahren")
        self.assertEqual(fahrrad.match_type, "normalized_match")

    def test_unknown_activity_returns_no_match(self):
        result = self.adapter.match_activity("stricken", self.canonical_names)

        self.assertFalse(result.matched)
        self.assertEqual(result.match_type, "no_match")
        self.assertEqual(result.normalized_input, "stricken")
        self.assertEqual(result.confidence, 0.0)


if __name__ == "__main__":
    unittest.main()
