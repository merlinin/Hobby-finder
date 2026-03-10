import unittest

from app import create_app
from knowledge_base.adapter import KnowledgeBaseAdapter


class KnowledgeBaseAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.adapter = KnowledgeBaseAdapter()

    def test_get_activity_attributes_for_known_activity(self):
        with self.app.app_context():
            hobby = self.adapter.get_hobby_by_name("Klettern")
            attributes = self.adapter.get_activity_attributes(hobby)

        self.assertGreater(len(attributes), 0)
        self.assertIn("körperlich", attributes)


    def test_get_activity_attributes_for_newly_seeded_activity(self):
        with self.app.app_context():
            hobby = self.adapter.get_hobby_by_name("Fotografie")
            attributes = self.adapter.get_activity_attributes(hobby)

        self.assertIsNotNone(hobby)
        self.assertIn("kreativ", attributes)
        self.assertGreaterEqual(attributes["kreativ"], 2)

    def test_get_activity_attributes_for_unknown_activity(self):
        with self.app.app_context():
            hobby = self.adapter.get_hobby_by_name("Unbekannt")
            attributes = self.adapter.get_activity_attributes(hobby)

        self.assertIsNone(hobby)
        self.assertEqual(attributes, {})


if __name__ == "__main__":
    unittest.main()
