import unittest

from personal_status.adapter import PersonalStatusAdapter
from personal_status.port import UserContext


class PersonalStatusAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.adapter = PersonalStatusAdapter()

    def test_active_hobby(self):
        result = self.adapter.derive(
            "qualified_hobby",
            UserContext(
                currently_active=True,
                frequency="regularly",
                personal_importance="high",
            ),
        )
        self.assertEqual(result.status, "active_hobby")

    def test_dormant_hobby(self):
        result = self.adapter.derive(
            "potential_hobby",
            UserContext(
                currently_active=False,
                previously_active=True,
                intends_to_resume=True,
            ),
        )
        self.assertEqual(result.status, "dormant_hobby")

    def test_former_hobby(self):
        result = self.adapter.derive(
            "qualified_hobby",
            UserContext(
                currently_active=False,
                previously_active=True,
                intends_to_resume=False,
            ),
        )
        self.assertEqual(result.status, "former_hobby")

    def test_emerging_interest(self):
        result = self.adapter.derive(
            "potential_hobby",
            UserContext(
                currently_active=True,
                frequency="rarely",
                personal_importance="medium",
            ),
        )
        self.assertEqual(result.status, "emerging_interest")

    def test_not_a_hobby_with_sufficient_negative_evidence(self):
        result = self.adapter.derive(
            "unlikely_hobby",
            UserContext(
                currently_active=False,
                previously_active=False,
                intends_to_resume=False,
                personal_importance="low",
            ),
        )
        self.assertEqual(result.status, "not_a_hobby")

    def test_missing_optional_fields_returns_insufficient_personal_context(self):
        result = self.adapter.derive("insufficient_evidence", UserContext())
        self.assertEqual(result.status, "insufficient_personal_context")

    def test_thin_context_returns_insufficient_personal_context(self):
        result = self.adapter.derive(
            "qualified_hobby",
            UserContext(personal_importance="low"),
        )
        self.assertEqual(result.status, "insufficient_personal_context")


if __name__ == "__main__":
    unittest.main()
