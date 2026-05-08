from pathlib import Path
from typing import Any

from .base import AgentAdapter
from agent_exam.core.task import TaskSpec


class MockAgent(AgentAdapter):
    name = "mock"

    def __init__(self, max_steps: int = 5, timeout_sec: int = 30) -> None:
        self.max_steps = max_steps
        self.timeout_sec = timeout_sec

    def run(self, task: TaskSpec, task_dir: Path) -> dict[str, Any]:
        if task.id == "basic_bugfix":
            return self._fix_basic_bugfix(task_dir)
        if task.id == "feature_addition":
            return self._add_feature(task_dir)
        return {
            "status": "no_recipe",
            "message": f"No mock recipe for task {task.id}",
            "changed_files": [],
        }

    def _fix_basic_bugfix(self, task_dir: Path) -> dict[str, Any]:
        target = task_dir / "repo" / "calculator.py"
        text = target.read_text(encoding="utf-8")
        updated = text.replace("return a - b", "return a + b")
        target.write_text(updated, encoding="utf-8")
        return {
            "status": "patched",
            "message": "Replaced subtraction with addition in add().",
            "changed_files": [str(target.relative_to(task_dir))],
            "token_usage": {"input_tokens": 0, "output_tokens": 0},
            "cost_usd": 0.0,
        }

    def _add_feature(self, task_dir: Path) -> dict[str, Any]:
        target = task_dir / "repo" / "text_utils.py"
        text = target.read_text(encoding="utf-8")
        if "def slugify(" not in text:
            text = text.rstrip() + "\n\n" + _SLUGIFY_FUNCTION
        target.write_text(text, encoding="utf-8")
        return {
            "status": "patched",
            "message": "Added slugify() to text_utils.",
            "changed_files": [str(target.relative_to(task_dir))],
            "token_usage": {"input_tokens": 0, "output_tokens": 0},
            "cost_usd": 0.0,
        }


_SLUGIFY_FUNCTION = '''def slugify(text):
    normalized = normalize_spaces(text).strip().lower()
    chars = []
    previous_dash = False
    for char in normalized:
        if char.isalnum():
            chars.append(char)
            previous_dash = False
        elif not previous_dash:
            chars.append("-")
            previous_dash = True
    return "".join(chars).strip("-")
'''
