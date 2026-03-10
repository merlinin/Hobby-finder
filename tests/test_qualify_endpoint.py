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
        self.assertEqual(payload["match"]["match_type"], "exact_alias")
        self.assertEqual(payload["match"]["activity_name"], "Klettern")
        self._assert_regression_fields(payload, "qualified_hobby")

    def test_qualify_new_alias_activity(self):
        response = self.client.post("/qualify", json={"activity": "mountainbike"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["match"]["match_type"], "exact_alias")
        self.assertEqual(payload["match"]["activity_name"], "Radfahren")
        self._assert_regression_fields(payload, "qualified_hobby")


    def test_qualify_capitalization_and_whitespace_variation(self):
        response = self.client.post("/qualify", json={"activity": "   kLeTtErN   "})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["match"]["matched"])
        self.assertEqual(payload["match"]["activity_name"], "Klettern")
        self.assertEqual(payload["match"]["match_type"], "exact_name")

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

    def test_qualify_unknown_activity(self):
        response = self.client.post("/qualify", json={"activity": "Space-Bongo"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertFalse(payload["match"]["matched"])
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

    def test_qualify_invalid_payload(self):
        response = self.client.post("/qualify", json={"activity": 42})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
