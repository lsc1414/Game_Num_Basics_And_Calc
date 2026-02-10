import unittest
from pathlib import Path


class TestDocsFixAllPipeline(unittest.TestCase):
    def test_runs_intro_style_check(self) -> None:
        script = Path("scripts/docs_fix_all.ps1").read_text(encoding="utf-8")
        self.assertIn(
            "check_doc_intro_style.py",
            script,
            "docs_fix_all.ps1 should invoke intro style checker.",
        )

    def test_auto_fix_requires_explicit_flag(self) -> None:
        script = Path("scripts/docs_fix_all.ps1").read_text(encoding="utf-8")
        self.assertIn(
            "[switch]$ApplyFix",
            script,
            "docs_fix_all.ps1 should require an explicit -ApplyFix flag for auto-fix.",
        )
        self.assertIn(
            "if ($ApplyFix)",
            script,
            "docs_fix_all.ps1 should guard auto-fix behind -ApplyFix.",
        )


if __name__ == "__main__":
    unittest.main()
