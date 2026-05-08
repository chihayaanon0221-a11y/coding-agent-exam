from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from agent_exam.core.result import ScoreResult
from agent_exam.core.task import TaskSpec


@dataclass
class ScoringContext:
    task: TaskSpec
    task_dir: Path
    original_repo: Path
    working_repo: Path
    run_dir: Path
    diff_text: str
    changed_files: list[str]
    diff_line_count: int


class Scorer(ABC):
    name = "base"

    @abstractmethod
    def score(self, context: ScoringContext) -> ScoreResult:
        raise NotImplementedError

