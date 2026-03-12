import unittest

from app import create_app
from models import Hobby, HobbyAttribute, db


class Phase2Slice5CuratedCasesTestCase(unittest.TestCase):
    """Small curated demo/regression set for meaningful pipeline states."""

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def _assert_stable_response_fields(
        self,
        payload: dict,
        *,
        expected_qualification: str,
        expected_personal_status: str,
        expected_matched: bool,
        expected_match_type: str,
    ) -> None:
        self.assertEqual(payload["qualification"]["status"], expected_qualification)
        self.assertEqual(payload["personal_status"], expected_personal_status)
        self.assertEqual(payload["match"]["matched"], expected_matched)
        self.assertEqual(payload["match"]["match_type"], expected_match_type)

        self.assertEqual(payload["explanation"], payload["general_explanation"])
        self.assertIsInstance(payload["general_explanation"], str)
        self.assertTrue(payload["general_explanation"])
        self.assertIsInstance(payload["personal_explanation"], str)
        self.assertTrue(payload["personal_explanation"])
        self.assertIsInstance(payload["matching_hint"], str)
        self.assertTrue(payload["matching_hint"])

    def _set_core_attribute_values(self, activity_name: str, values: dict[str, int]) -> list[tuple[int, int]]:
        with self.app.app_context():
            hobby = Hobby.query.filter_by(name=activity_name).first()
            self.assertIsNotNone(hobby)

            originals: list[tuple[int, int]] = []
            for hobby_attribute in hobby.attributes:
                attribute_name = hobby_attribute.attribute.name.lower()
                if attribute_name in values:
                    originals.append((hobby_attribute.id, hobby_attribute.value))
                    hobby_attribute.value = values[attribute_name]
            db.session.commit()
            return originals

    def _restore_attribute_values(self, originals: list[tuple[int, int]]) -> None:
        with self.app.app_context():
            for hobby_attribute_id, previous_value in originals:
                persisted = db.session.get(HobbyAttribute, hobby_attribute_id)
                persisted.value = previous_value
            db.session.commit()

    def test_curated_clear_hobby_case(self):
        response = self.client.post("/qualify", json={"activity": "Klettern"})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="qualified_hobby",
            expected_personal_status="insufficient_personal_context",
            expected_matched=True,
            expected_match_type="exact_match",
        )

    def test_curated_potential_hobby_borderline_case(self):
        originals = self._set_core_attribute_values(
            "Kochen",
            {"freiwillig": 3, "freizeit": 1, "regelmäßig": 1},
        )

        try:
            response = self.client.post("/qualify", json={"activity": "Kochen"})
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self._assert_stable_response_fields(
                payload,
                expected_qualification="potential_hobby",
                expected_personal_status="insufficient_personal_context",
                expected_matched=True,
                expected_match_type="exact_match",
            )
        finally:
            self._restore_attribute_values(originals)

    def test_curated_dormant_hobby_case(self):
        response = self.client.post(
            "/qualify",
            json={
                "activity": "Klettern",
                "currently_active": False,
                "previously_active": True,
                "intends_to_resume": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="qualified_hobby",
            expected_personal_status="dormant_hobby",
            expected_matched=True,
            expected_match_type="exact_match",
        )

    def test_curated_former_hobby_case(self):
        response = self.client.post(
            "/qualify",
            json={
                "activity": "Klettern",
                "currently_active": False,
                "previously_active": True,
                "intends_to_resume": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="qualified_hobby",
            expected_personal_status="former_hobby",
            expected_matched=True,
            expected_match_type="exact_match",
        )

    def test_curated_emerging_interest_case(self):
        response = self.client.post(
            "/qualify",
            json={
                "activity": "Klettern",
                "currently_active": True,
                "frequency": "rarely",
                "personal_importance": "medium",
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="qualified_hobby",
            expected_personal_status="emerging_interest",
            expected_matched=True,
            expected_match_type="exact_match",
        )

    def test_curated_thin_personal_context_case(self):
        response = self.client.post(
            "/qualify",
            json={"activity": "Klettern", "personal_importance": "low"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="qualified_hobby",
            expected_personal_status="insufficient_personal_context",
            expected_matched=True,
            expected_match_type="exact_match",
        )

    def test_curated_no_match_case(self):
        response = self.client.post("/qualify", json={"activity": "Space-Bongo"})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="insufficient_evidence",
            expected_personal_status="insufficient_personal_context",
            expected_matched=False,
            expected_match_type="no_match",
        )

    def test_curated_alias_match_case(self):
        response = self.client.post("/qualify", json={"activity": "bouldern"})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self._assert_stable_response_fields(
            payload,
            expected_qualification="qualified_hobby",
            expected_personal_status="insufficient_personal_context",
            expected_matched=True,
            expected_match_type="alias_match",
        )


if __name__ == "__main__":
    unittest.main()
