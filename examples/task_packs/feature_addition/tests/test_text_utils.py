import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "repo"))

from text_utils import normalize_spaces, slugify


class TextUtilsTests(unittest.TestCase):
    def test_normalize_spaces_existing_behavior(self):
        self.assertEqual(normalize_spaces("a   b\tc"), "a b c")

    def test_slugify_simple_text(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_slugify_punctuation_and_case(self):
        self.assertEqual(slugify("  Agent, Eval!  "), "agent-eval")

    def test_slugify_empty_text(self):
        self.assertEqual(slugify("   "), "")


if __name__ == "__main__":
    unittest.main()

