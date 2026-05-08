import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TaskSpec:
    id: str
    title: str
    scenario: str
    difficulty: str
    repo_path: str
    instructions: str
    success_criteria: list[str]
    allowed_tools: list[str]
    expected_outputs: list[str]
    scoring_profile: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_task_spec(task_pack_path: Path) -> TaskSpec:
    task_path = task_pack_path / "task.yaml"
    if not task_path.exists():
        raise FileNotFoundError(f"missing task spec: {task_path}")

    text = task_path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "task.yaml must use the JSON-compatible YAML subset in this stdlib-only harness"
        ) from exc

    return TaskSpec(
        id=str(data["id"]),
        title=str(data["title"]),
        scenario=str(data["scenario"]),
        difficulty=str(data["difficulty"]),
        repo_path=str(data["repo_path"]),
        instructions=str(data["instructions"]),
        success_criteria=[str(item) for item in data.get("success_criteria", [])],
        allowed_tools=[str(item) for item in data.get("allowed_tools", [])],
        expected_outputs=[str(item) for item in data.get("expected_outputs", [])],
        scoring_profile=dict(data.get("scoring_profile", {})),
    )

