"""Tests for gate_check.py (stdlib unittest, no network). Run: python3 test_gate_check.py"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).with_name("gate_check.py")
GOOD_REPORT = """# Release report: demo @ abc123 (staging)
| check | status | evidence | impact | fix task |
|---|---|---|---|---|
| G7 | PASS | served hash == export hash, see deploy.log:12 | none | - |
| G9 | FAIL | `prisma migrate status` shows drift, see migrate.log:3 | blocks ship | Fix 1 |
| G6 | NOT ASSESSED | no android build in scope | none | - |
"""
GOOD_FIX = """# Fix plan: demo @ abc123
### Fix 1: migration drift [blocks SHIP]
- Check: G9 | Severity: High
- Files: prisma/schema.prisma
- Commands: `prisma migrate status` (expect clean)
- Acceptance: `prisma migrate status` exits 0 on staging
"""


def run_gate(d):
    return subprocess.run([sys.executable, str(GATE, ), str(d)],
                          capture_output=True, text=True)


def write(d, name, content):
    p = Path(d) / name
    p.write_text(content)
    return p


class TestGateCheck(unittest.TestCase):
    def test_valid_pair_passes(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "report.md", GOOD_REPORT)
            write(d, "fix-plan.md", GOOD_FIX)
            r = run_gate(d)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("GATE PASS", r.stdout)

    def test_empty_dir_passes(self):
        with tempfile.TemporaryDirectory() as d:
            r = run_gate(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_fail_without_acceptance(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "report.md", GOOD_REPORT)
            write(d, "fix-plan.md", GOOD_FIX.replace("- Acceptance:", "- Someday:"))
            r = run_gate(d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("Acceptance", r.stdout)

    def test_fail_without_fix_section(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "report.md", GOOD_REPORT)
            r = run_gate(d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("lacks Fix+Acceptance", r.stdout)

    def test_pass_without_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "report.md", "| check | status | evidence |\n| G1 | PASS | trust me |\n")
            r = run_gate(d)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("without evidence", r.stdout)

    def test_row_without_evidence_or_reason(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "report.md", "| check | status |\n| G2 | FAIL |\n")
            r = run_gate(d)
            self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
