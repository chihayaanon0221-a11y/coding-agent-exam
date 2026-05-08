from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ScoreResult:
    scorer_name: str
    score: float
    max_score: float
    passed: bool
    evidence: dict[str, Any] = field(default_factory=dict)
    comments: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def normalized(self) -> float:
        if self.max_score <= 0:
            return 0.0
        return max(0.0, min(1.0, self.score / self.max_score))

    @property
    def skipped(self) -> bool:
        return bool(self.evidence.get("skipped"))


@dataclass
class RunResult:
    run_id: str
    task_id: str
    agent_name: str
    started_at: str
    ended_at: str
    status: str
    scores: list[ScoreResult]
    artifacts: dict[str, str]
    trace_path: str
    report_path: str
    errors: list[str] = field(default_factory=list)
    final_score: float = 0.0
    failure_taxonomy: list[str] = field(default_factory=list)
    scenario: str = ""
    difficulty: str = ""
    task_pack_path: str = ""
    run_config: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["scores"] = [score.to_dict() for score in self.scores]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunResult":
        scores = [ScoreResult(**score) for score in data.get("scores", [])]
        copied = dict(data)
        copied["scores"] = scores
        return cls(**copied)
