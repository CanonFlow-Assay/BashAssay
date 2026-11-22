import subprocess
import unittest


class Arguments(unittest.TestCase):
    def test_preserves_spaces_dashes_and_globs(self):
        result = subprocess.run(
            ["bash", "--noprofile", "--norc", "./arguments.sh", "two words", "-flag", "*.csv"],
            capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, b"two words\n-flag\n*.csv\n")

    def test_empty_arguments_have_no_output(self):
        result = subprocess.run(
            ["bash", "--noprofile", "--norc", "./arguments.sh"],
            capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout, b"")


if __name__ == "__main__":
    unittest.main()
