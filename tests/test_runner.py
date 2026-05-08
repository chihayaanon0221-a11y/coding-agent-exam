import tempfile
import unittest
from pathlib import Path

from agent_exam.core.run import run_task_pack


class RunnerTests(unittest.TestCase):
    def test_mock_agent_generates_basic_bugfix_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_task_pack(
                task_pack_path=Path("examples/task_packs/basic_bugfix"),
                agent_name="mock",
                output_dir=Path(tmp),
                run_id="test-run",
            )

            self.assertEqual(result.status, "passed")
            self.assertGreaterEqual(result.final_score, 0.8)
            self.assertTrue(Path(result.report_path).exists())
            self.assertTrue(Path(result.trace_path).exists())
            self.assertTrue(Path(result.artifacts["result_json"]).exists())
            self.assertIn("workspace", result.artifacts["workspace"])
            original = Path("examples/task_packs/basic_bugfix/repo/calculator.py").read_text(
                encoding="utf-8"
            )
            self.assertIn("return a - b", original)


if __name__ == "__main__":
    unittest.main()
