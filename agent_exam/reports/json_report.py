import json
from pathlib import Path

from agent_exam.core.result import RunResult


def write_result_json(path: Path, result: RunResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

