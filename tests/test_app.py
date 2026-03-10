import unittest

from app import create_app


class AppRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_page_renders_qualification_demo(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("Hobby Finder – Activity Qualification Demo", body)
        self.assertIn("Welche Tätigkeit möchtest du prüfen?", body)
        self.assertIn("/qualify", body)


    def test_hobbies_endpoint_returns_expected_structure(self):
        response = self.client.get("/hobbies")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, list)
        self.assertGreater(len(payload), 0)
        first = payload[0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.assertIn("category", first)
        self.assertIn("notes", first)
        self.assertIn("attributes", first)

    def test_attributes_endpoint_returns_sorted_names(self):
        response = self.client.get("/attributes")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, list)
        names = [item["name"] for item in payload]
        self.assertEqual(names, sorted(names))

    def test_wordcloud_png_endpoint_returns_image(self):
        response = self.client.get("/wordcloud.png")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")
        self.assertGreater(len(response.data), 1000)


if __name__ == "__main__":
    unittest.main()
