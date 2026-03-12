import unittest

from app import create_app
from models import Hobby, HobbyAttribute, db


class QualifyEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

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

    def _assert_regression_fields(self, payload: dict, expected_status: str) -> None:
        self.assertEqual(payload["qualification"]["status"], expected_status)
        self.assertIn("status", payload["qualification"])
        self.assertIn("label", payload["qualification"])
        self.assertIn("score", payload["qualification"])
        self.assertIn("supporting_attributes", payload["qualification"])
        self.assertIn("missing_or_weak_attributes", payload["qualification"])
        self.assertIn("personal_status", payload)
        self.assertIn("general_explanation", payload)
        self.assertIn("personal_explanation", payload)
        self.assertIn("matching_hint", payload)
        self.assertEqual(payload["explanation"], payload["general_explanation"])

    def test_qualify_known_activity(self):
        response = self.client.post("/qualify", json={"activity": "Klettern"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["match"]["matched"])
        self._assert_regression_fields(payload, "qualified_hobby")

    def test_qualify_alias_activity(self):
        response = self.client.post("/qualify", json={"activity": "bouldern"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["match"]["match_type"], "alias_match")
        self.assertEqual(payload["match"]["activity_name"], "Klettern")
        self.assertIn("Alias", payload["matching_hint"])
        self._assert_regression_fields(payload, "qualified_hobby")

    def test_qualify_new_alias_activity(self):
        response = self.client.post("/qualify", json={"activity": "mountainbike"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["match"]["match_type"], "alias_match")
        self.assertEqual(payload["match"]["activity_name"], "Radfahren")
        self._assert_regression_fields(payload, "qualified_hobby")



    def test_qualify_phase2_slice3_alias_coverage(self):
        alias_cases = {
            "yoga machen": "Yoga",
            "hiken": "Wandern",
            "piano": "Klavier spielen",
            "loeten": "Elektronik basteln",
            "philatelie": "Briefmarken sammeln",
            "birdwatching": "Vogelbeobachtung",
        }

        for user_input, expected_activity in alias_cases.items():
            with self.subTest(user_input=user_input):
                response = self.client.post("/qualify", json={"activity": user_input})
                self.assertEqual(response.status_code, 200)
                payload = response.get_json()
                self.assertTrue(payload["match"]["matched"])
                self.assertEqual(payload["match"]["activity_name"], expected_activity)
                self.assertEqual(payload["match"]["match_type"], "alias_match")
                self._assert_regression_fields(payload, "qualified_hobby")

    def test_qualify_capitalization_and_whitespace_variation(self):
        response = self.client.post("/qualify", json={"activity": "   kLeTtErN   "})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["match"]["matched"])
        self.assertEqual(payload["match"]["activity_name"], "Klettern")
        self.assertEqual(payload["match"]["match_type"], "exact_match")
        self.assertEqual(payload["match"]["normalized_input"], "klettern")

    def test_qualify_hyphen_and_punctuation_variation(self):
        response = self.client.post("/qualify", json={"activity": "3D-Druck!"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["match"]["matched"])
        self.assertEqual(payload["match"]["activity_name"], "3D-Druck")

    def test_qualify_simple_phrase_variants(self):
        phrase_cases = {
            "klettern gehen": "Klettern",
            "musik machen": "Musik machen",
            "fahrrad fahren": "Radfahren",
        }

        for user_input, expected_activity in phrase_cases.items():
            with self.subTest(user_input=user_input):
                response = self.client.post("/qualify", json={"activity": user_input})
                self.assertEqual(response.status_code, 200)
                payload = response.get_json()
                self.assertTrue(payload["match"]["matched"])
                self.assertEqual(payload["match"]["activity_name"], expected_activity)
                if user_input in {"klettern gehen", "fahrrad fahren"}:
                    self.assertEqual(payload["match"]["match_type"], "normalized_match")

    def test_qualify_unknown_activity(self):
        response = self.client.post("/qualify", json={"activity": "Space-Bongo"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertFalse(payload["match"]["matched"])
        self.assertEqual(payload["match"]["match_type"], "no_match")
        self.assertEqual(payload["match"]["normalized_input"], "space bongo")
        self.assertIn("Kein belastbarer Treffer", payload["matching_hint"])
        self._assert_regression_fields(payload, "insufficient_evidence")
        self.assertEqual(payload["attributes"], {})

    def test_qualify_potential_hobby_with_weaker_seeded_activity_profile(self):
        originals = self._set_core_attribute_values(
            "Kochen",
            {"freiwillig": 3, "freizeit": 1, "regelmäßig": 1},
        )

        try:
            response = self.client.post("/qualify", json={"activity": "Kochen"})
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()
            self._assert_regression_fields(payload, "potential_hobby")
        finally:
            self._restore_attribute_values(originals)

    def test_qualify_unlikely_hobby_with_weak_seeded_activity_profile(self):
        originals = self._set_core_attribute_values(
            "Radfahren",
            {"freiwillig": 1, "freizeit": 1, "regelmäßig": 0},
        )

        try:
            response = self.client.post("/qualify", json={"activity": "Radfahren"})
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()
            self._assert_regression_fields(payload, "unlikely_hobby")
        finally:
            self._restore_attribute_values(originals)

    def test_qualify_response_structure(self):
        response = self.client.post("/qualify", json={"activity": "Klettern"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("input", payload)
        self.assertIn("match", payload)
        self.assertIn("qualification", payload)
        self.assertIn("attributes", payload)
        self.assertIn("explanation", payload)
        self.assertIn("supporting_attributes", payload["qualification"])
        self.assertIn("missing_or_weak_attributes", payload["qualification"])
        self.assertIn("personal_status", payload)
        self.assertIn("general_explanation", payload)
        self.assertIn("personal_explanation", payload)
        self.assertIn("matching_hint", payload)

    def test_qualify_with_personal_context_returns_active_hobby(self):
        response = self.client.post(
            "/qualify",
            json={
                "activity": "Klettern",
                "currently_active": True,
                "frequency": "regularly",
                "personal_importance": "high",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["personal_status"], "active_hobby")
        self.assertIn("active_hobby", payload["personal_explanation"])
        self.assertIn("Allgemeine Einschätzung", payload["general_explanation"])

    def test_qualify_with_former_context_returns_former_hobby(self):
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
        self.assertEqual(payload["personal_status"], "former_hobby")

    def test_qualify_with_dormant_context_returns_dormant_hobby(self):
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
        self.assertEqual(payload["personal_status"], "dormant_hobby")

    def test_qualify_with_missing_optional_context_fields_returns_context_status(self):
        response = self.client.post("/qualify", json={"activity": "Klettern"})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["personal_status"], "insufficient_personal_context")
        self.assertIn("insufficient_personal_context", payload["personal_explanation"])

    def test_qualify_with_thin_context_does_not_default_to_not_a_hobby(self):
        response = self.client.post(
            "/qualify",
            json={"activity": "Klettern", "personal_importance": "low"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["personal_status"], "insufficient_personal_context")

    def test_qualify_with_negative_personal_evidence_returns_not_a_hobby(self):
        response = self.client.post(
            "/qualify",
            json={
                "activity": "Space-Bongo",
                "currently_active": False,
                "previously_active": False,
                "intends_to_resume": False,
                "personal_importance": "low",
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["qualification"]["status"], "insufficient_evidence")
        self.assertEqual(payload["personal_status"], "not_a_hobby")

    def test_qualify_rejects_invalid_frequency(self):
        response = self.client.post("/qualify", json={"activity": "Klettern", "frequency": "daily"})
        self.assertEqual(response.status_code, 400)

    def test_qualify_rejects_invalid_context_type(self):
        response = self.client.post("/qualify", json={"activity": "Klettern", "currently_active": "yes"})
        self.assertEqual(response.status_code, 400)

    def test_qualify_invalid_payload(self):
        response = self.client.post("/qualify", json={"activity": 42})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
