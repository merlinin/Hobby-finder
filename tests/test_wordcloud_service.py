import unittest
from unittest.mock import patch

import wordcloud_service


class WordcloudServiceTestCase(unittest.TestCase):
    def test_get_top_words_filters_noise_and_merges_variants(self):
        sample = """
        ausübt ausgeübt auszuüben freiwillige freiwilligen working free time one especially
        freizeit interesse neigungen leidenschaften
        """
        with patch.object(wordcloud_service, "_load_source_text", return_value=sample):
            top = dict(wordcloud_service.get_top_words(top_n=20))

        self.assertEqual(top.get("ausüben"), 3)
        self.assertEqual(top.get("freiwillig"), 2)
        self.assertIn("freizeit", top)
        self.assertNotIn("working", top)

    def test_word_color_category_mapping(self):
        self.assertEqual(wordcloud_service._word_color("ausüben"), "#2f6fed")
        self.assertEqual(wordcloud_service._word_color("interesse"), "#2e8b57")
        self.assertEqual(wordcloud_service._word_color("entspannung"), "#f08c00")
        self.assertEqual(wordcloud_service._word_color("regelmäßig"), "#6c757d")


if __name__ == "__main__":
    unittest.main()
