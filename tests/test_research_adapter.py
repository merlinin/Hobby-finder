import unittest
from unittest.mock import MagicMock

from research.adapter import ResearchAdapter


class ResearchAdapterTestCase(unittest.TestCase):
    def test_get_top_words_delegates_without_transforming(self):
        expected = [("ausüben", 3), ("freizeit", 2)]
        mock_get_top_words = MagicMock(return_value=expected)
        adapter = ResearchAdapter(get_top_words_fn=mock_get_top_words)

        result = adapter.get_top_words(top_n=15)

        mock_get_top_words.assert_called_once_with(top_n=15)
        self.assertEqual(result, expected)

    def test_generate_wordcloud_image_delegates_without_transforming(self):
        sentinel_image = object()
        mock_generate = MagicMock(return_value=sentinel_image)
        adapter = ResearchAdapter(generate_wordcloud_image_fn=mock_generate)

        result = adapter.generate_wordcloud_image()

        mock_generate.assert_called_once_with()
        self.assertIs(result, sentinel_image)


if __name__ == "__main__":
    unittest.main()
