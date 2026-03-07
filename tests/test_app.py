import unittest

from app import create_app


class AppRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_page_renders_wordcloud_section(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("Wordcloud", body)
        self.assertIn("/wordcloud.png", body)

    def test_wordcloud_png_endpoint_returns_image(self):
        response = self.client.get("/wordcloud.png")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")
        self.assertGreater(len(response.data), 1000)


if __name__ == "__main__":
    unittest.main()
