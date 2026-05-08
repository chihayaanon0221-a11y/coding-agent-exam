from pathlib import Path
from typing import Any

from agent_exam.core.result import ScoreResult
from agent_exam.scorers.base import Scorer, ScoringContext


class RuleScorer(Scorer):
    name = "rule"

    def score(self, context: ScoringContext) -> ScoreResult:
        profile = context.task.scoring_profile
        checks: list[tuple[str, bool]] = []

        for rel_path in profile.get("required_files", []):
            path = context.task_dir / str(rel_path)
            checks.append((f"required file exists: {rel_path}", path.exists()))

        for rel_path in profile.get("forbidden_files", []):
            path = context.task_dir / str(rel_path)
            checks.append((f"forbidden file absent: {rel_path}", not path.exists()))

        for item in profile.get("required_text_patterns", []):
            rel_path, pattern = _pattern_item(item)
            text = _read(context.task_dir / rel_path)
            checks.append((f"required text in {rel_path}: {pattern}", pattern in text))

        for item in profile.get("forbidden_text_patterns", []):
            rel_path, pattern = _pattern_item(item)
            text = _read(context.task_dir / rel_path)
            checks.append((f"forbidden text absent in {rel_path}: {pattern}", pattern not in text))

        if not checks:
            return ScoreResult(
                scorer_name=self.name,
                score=1.0,
                max_score=1.0,
                passed=True,
                evidence={"checks": []},
                comments="No rule checks configured.",
            )

        passed_count = sum(1 for _, passed in checks if passed)
        score = passed_count / len(checks)
        return ScoreResult(
            scorer_name=self.name,
            score=score,
            max_score=1.0,
            passed=passed_count == len(checks),
            evidence={"checks": [{"name": name, "passed": passed} for name, passed in checks]},
            comments=f"{passed_count}/{len(checks)} rule checks passed.",
        )


def _pattern_item(item: Any) -> tuple[Path, str]:
    if isinstance(item, dict):
        return Path(str(item["path"])), str(item["pattern"])
    if isinstance(item, list) and len(item) == 2:
        return Path(str(item[0])), str(item[1])
    raise ValueError(f"invalid pattern item: {item!r}")


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

