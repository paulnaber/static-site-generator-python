import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world  "), "Hello world")

    def test_extract_title_ignores_other_headings(self):
        with self.assertRaises(Exception):
            extract_title("## Not an h1")


if __name__ == "__main__":
    unittest.main()