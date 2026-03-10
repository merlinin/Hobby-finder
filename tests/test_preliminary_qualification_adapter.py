import unittest

from qualification.adapter import PreliminaryQualificationAdapter


class PreliminaryQualificationAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.adapter = PreliminaryQualificationAdapter()

    def test_clear_hobby_like_activity_is_qualified(self):
        result = self.adapter.qualify(
            matched=True,
            attributes={
                "freiwillig": 3,
                "freizeit": 3,
                "regelmäßig": 2,
                "kreativ": 2,
            },
        )

        self.assertEqual(result.status, "qualified_hobby")
        self.assertGreaterEqual(result.score, 0.6)
        self.assertIn("freiwillig (3)", result.supporting_attributes)

    def test_borderline_activity_is_potential_hobby(self):
        result = self.adapter.qualify(
            matched=True,
            attributes={
                "freiwillig": 3,
                "freizeit": 1,
                "regelmäßig": 1,
                "kreativ": 2,
            },
        )

        self.assertEqual(result.status, "potential_hobby")
        self.assertIn("freizeit (1)", result.missing_or_weak_attributes)

    def test_insufficient_evidence_when_core_attributes_are_missing(self):
        result = self.adapter.qualify(
            matched=True,
            attributes={"kreativ": 2, "drinnen": 3},
        )

        self.assertEqual(result.status, "insufficient_evidence")
        self.assertEqual(result.support_strength, "limited")

    def test_unlikely_hobby_when_core_attributes_are_consistently_weak(self):
        result = self.adapter.qualify(
            matched=True,
            attributes={"freiwillig": 1, "freizeit": 1, "regelmäßig": 0, "kreativ": 2},
        )

        self.assertEqual(result.status, "unlikely_hobby")
        self.assertIn("regelmäßig (0)", result.missing_or_weak_attributes)

    def test_unmatched_activity_is_insufficient_evidence(self):
        result = self.adapter.qualify(matched=False, attributes={})
        self.assertEqual(result.status, "insufficient_evidence")
        self.assertTrue(result.preliminary)


if __name__ == "__main__":
    unittest.main()
