import unittest
from pathlib import Path

from agent_exam.core.task import load_task_spec
from agent_exam.cli import discover_task_packs


class TaskLoadingTests(unittest.TestCase):
    def test_loads_basic_bugfix_task(self):
        task = load_task_spec(Path("examples/task_packs/basic_bugfix"))
        self.assertEqual(task.id, "basic_bugfix")
        self.assertEqual(task.scenario, "bugfix")
        self.assertIn("test_command", task.scoring_profile)

    def test_discovers_task_pack_directory(self):
        packs = discover_task_packs(Path("examples/task_packs"))
        names = [path.name for path in packs]
        self.assertEqual(names, ["basic_bugfix", "feature_addition"])


if __name__ == "__main__":
    unittest.main()
