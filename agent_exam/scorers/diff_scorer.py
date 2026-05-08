import difflib
from pathlib import Path

from agent_exam.core.result import ScoreResult
from agent_exam.scorers.base import Scorer, ScoringContext
from agent_exam.utils.fs import iter_files


class DiffScorer(Scorer):
    name = "diff"

    def score(self, context: ScoringContext) -> ScoreResult:
        max_diff_lines = int(context.task.scoring_profile.get("max_diff_lines", 200))
        diff_lines = context.diff_line_count
        if diff_lines == 0:
            score = 0.0
            passed = False
            comments = "No repo changes detected."
        elif diff_lines <= max_diff_lines:
            score = 1.0
            passed = True
            comments = "Diff size is within the configured limit."
        else:
            score = max(0.0, 1.0 - ((diff_lines - max_diff_lines) / max_diff_lines))
            passed = False
            comments = "Diff exceeds the configured limit."

        return ScoreResult(
            scorer_name=self.name,
            score=score,
            max_score=1.0,
            passed=passed,
            evidence={
                "original_repo": str(context.original_repo),
                "working_repo": str(context.working_repo),
                "diff_lines": diff_lines,
                "max_diff_lines": max_diff_lines,
                "changed_files": context.changed_files,
            },
            comments=comments,
        )


def build_repo_diff(original_repo: Path, working_repo: Path) -> tuple[str, list[str], int]:
    original_files = {_relative(path, original_repo): path for path in iter_files(original_repo)}
    working_files = {_relative(path, working_repo): path for path in iter_files(working_repo)}
    all_paths = sorted(set(original_files) | set(working_files))
    chunks: list[str] = []
    changed_files: list[str] = []

    for rel_path in all_paths:
        before = _read_lines(original_files.get(rel_path))
        after = _read_lines(working_files.get(rel_path))
        if before == after:
            continue
        changed_files.append(rel_path)
        chunks.extend(
            difflib.unified_diff(
                before,
                after,
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            )
        )

    diff_text = "\n".join(chunks)
    diff_line_count = len([line for line in chunks if line.startswith("+") or line.startswith("-")])
    return diff_text + ("\n" if diff_text else ""), changed_files, diff_line_count


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_lines(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return []
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return ["<binary file>"]
