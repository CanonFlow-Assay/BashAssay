"""Native source is data while scanning a declared file."""

import os
import unittest

import test_assay


class StaticExecutionBoundary(test_assay.ConsumerFixture, unittest.TestCase):
    def test_inspection_never_executes_the_target_script(self):
        marker = self.cwd / "script-executed"
        (self.cwd / self.source_name).write_text(f"printf '%s\\n' exercised > '{marker}'\n")
        receipt = self.invoke("scan", 2)
        self.assertTrue(receipt["sources"][0]["checks"])
        self.assertFalse(marker.exists())

    def test_ambient_shell_hooks_and_analyzer_options_are_ignored(self):
        marker = self.cwd / "startup-executed"
        startup = self.cwd / "startup.sh"
        startup.write_text(f"touch -- '{marker}'\n")
        (self.cwd / ".shellcheckrc").write_text("disable=SC2086\n")
        (self.cwd / self.source_name).write_text('printf "%s\\n" $1\n')
        env = dict(os.environ, BASH_ENV=str(startup), SHELLCHECK_OPTS="--exclude=SC2086")
        receipt = self.invoke("scan", 1, env=env)
        self.assertIn("BA007", {finding["ruleId"] for finding in receipt["sources"][0]["findings"]})
        self.assertFalse(marker.exists())
