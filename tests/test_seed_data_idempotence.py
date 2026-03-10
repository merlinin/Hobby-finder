import unittest

from app import create_app
from models import Hobby, HobbyAttribute, db, seed_data


class SeedDataIdempotenceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True

    def test_seed_data_is_idempotent_for_hobbies_and_links(self):
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # fresh database
            seed_data()
            hobby_count_first = Hobby.query.count()
            hobby_attribute_count_first = HobbyAttribute.query.count()
            hobby_names_first = [h.name for h in Hobby.query.order_by(Hobby.name).all()]

            # already seeded database
            seed_data()
            hobby_count_second = Hobby.query.count()
            hobby_attribute_count_second = HobbyAttribute.query.count()
            hobby_names_second = [h.name for h in Hobby.query.order_by(Hobby.name).all()]

            self.assertEqual(hobby_count_first, hobby_count_second)
            self.assertEqual(hobby_attribute_count_first, hobby_attribute_count_second)
            self.assertEqual(hobby_names_first, hobby_names_second)
            self.assertEqual(len(hobby_names_second), len(set(hobby_names_second)))

    def test_seed_data_contains_expanded_activities(self):
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            seed_data()

            names = {h.name for h in Hobby.query.all()}

        self.assertIn("Fotografie", names)
        self.assertIn("Gitarre spielen", names)
        self.assertIn("Radfahren", names)


if __name__ == "__main__":
    unittest.main()
