import unittest
from srt_audit.cli import validate, parse_timestamp

GOOD = "1\n00:00:00,000 --> 00:00:01,500\nHello world\n\n2\n00:00:01,500 --> 00:00:03,000\nNext line\n"

class ValidatorTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate(GOOD), [])

    def test_overlap(self):
        overlapping = GOOD.replace("00:00:01,500 --> 00:00:03,000", "00:00:01,000 --> 00:00:03,000")
        self.assertIn("overlap", [issue["code"] for issue in validate(overlapping)])

    def test_invalid_timestamp(self):
        self.assertIsNone(parse_timestamp("00:61:00,000"))

    def test_bad_sequence(self):
        self.assertIn("index", [issue["code"] for issue in validate(GOOD.replace("\n2\n", "\n4\n"))])

    def test_empty(self):
        self.assertEqual(validate(" ")[0]["code"], "empty")

if __name__ == "__main__":
    unittest.main()
