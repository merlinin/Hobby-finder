import unittest

from app import create_app


class QualifyEndpointTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_qualify_known_activity(self):
        response = self.client.post("/qualify", json={"activity": "Klettern"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["match"]["matched"])
        self.assertEqual(payload["qualification"]["label"], "potential_hobby_candidate")

    def test_qualify_alias_activity(self):
        response = self.client.post("/qualify", json={"activity": "bouldern"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["match"]["match_type"], "exact_alias")
        self.assertEqual(payload["match"]["activity_name"], "Klettern")

    def test_qualify_unknown_activity(self):
        response = self.client.post("/qualify", json={"activity": "Space-Bongo"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertFalse(payload["match"]["matched"])
        self.assertEqual(payload["qualification"]["label"], "unknown_activity")
        self.assertEqual(payload["attributes"], {})

    def test_qualify_response_structure(self):
        response = self.client.post("/qualify", json={"activity": "Klettern"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("input", payload)
        self.assertIn("match", payload)
        self.assertIn("qualification", payload)
        self.assertIn("attributes", payload)
        self.assertIn("explanation", payload)

    def test_qualify_invalid_payload(self):
        response = self.client.post("/qualify", json={"activity": 42})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
