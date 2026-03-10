import unittest

from qualification.adapter import PreliminaryQualificationAdapter


class PreliminaryQualificationAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.adapter = PreliminaryQualificationAdapter()

    def test_unknown_activity_when_not_matched(self):
        result = self.adapter.qualify(matched=False, attributes={})
        self.assertEqual(result.label, "unknown_activity")
        self.assertTrue(result.preliminary)

    def test_known_activity_when_no_attributes_present(self):
        result = self.adapter.qualify(matched=True, attributes={})
        self.assertEqual(result.label, "known_activity")
        self.assertTrue(result.preliminary)

    def test_potential_candidate_when_attributes_present(self):
        result = self.adapter.qualify(matched=True, attributes={"kreativ": 2})
        self.assertEqual(result.label, "potential_hobby_candidate")
        self.assertTrue(result.preliminary)


if __name__ == "__main__":
    unittest.main()
