import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from agent_exam.adapters.mock_agent import MockAgent
from agent_exam.core.result import RunResult, ScoreResult
from agent_exam.core.task import TaskSpec, load_task_spec
from agent_exam.core.trace import TraceWriter, utc_now
from agent_exam.reports.json_report import write_result_json
from agent_exam.reports.markdown import write_markdown_report
from agent_exam.scorers.base import ScoringContext
from agent_exam.scorers.diff_scorer import DiffScorer, build_repo_diff
from agent_exam.scorers.llm_judge_scorer import LLMJudgeScorer
from agent_exam.scorers.rule_scorer import RuleScorer
from agent_exam.scorers.test_scorer import TestScorer


@dataclass
class RunConfig:
    task_pack_path: str
    agent_name: str
    max_steps: int
    timeout_sec: int
    output_dir: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def make_run_id(task_id: str, agent_name: str) -> str:
    stamp = utc_now().replace(":", "").replace(".", "").replace("+", "Z")
    return f"{task_id}-{agent_name}-{stamp}"


def run_task_pack(
    task_pack_path: Path,
    agent_name: str,
    output_dir: Path,
    run_id: str | None = None,
    max_steps: int = 5,
    timeout_sec: int = 30,
) -> RunResult:
    task = load_task_spec(task_pack_path)
    config = RunConfig(
        task_pack_path=str(task_pack_path),
        agent_name=agent_name,
        max_steps=max_steps,
        timeout_sec=timeout_sec,
        output_dir=str(output_dir),
    )
    actual_run_id = run_id or make_run_id(task.id, agent_name)
    run_dir = output_dir / actual_run_id
    task_dir = run_dir / "workspace"
    original_repo = task_pack_path / task.repo_path
    working_repo = task_dir / task.repo_path
    trace_path = run_dir / "trace.jsonl"
    started_at = utc_now()
    errors: list[str] = []

    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(task_pack_path, task_dir)

    trace = TraceWriter(trace_path, task.id)
    trace.emit("task_loaded", "Loaded task specification", {"run_config": config.to_dict()})

    if agent_name != "mock":
        raise ValueError("Only the mock agent is implemented in this local harness")

    agent = MockAgent(max_steps=max_steps, timeout_sec=timeout_sec)
    trace.emit("agent_start", "Starting mock agent", {"agent": agent.name})
    agent_result = agent.run(task, task_dir)
    trace.emit("agent_finish", "Mock agent finished", agent_result)

    diff_text, changed_files, diff_line_count = build_repo_diff(original_repo, working_repo)
    patch_path = run_dir / "patch.diff"
    patch_path.write_text(diff_text, encoding="utf-8")

    context = ScoringContext(
        task=task,
        task_dir=task_dir,
        original_repo=original_repo,
        working_repo=working_repo,
        run_dir=run_dir,
        diff_text=diff_text,
        changed_files=changed_files,
        diff_line_count=diff_line_count,
    )

    scores: list[ScoreResult] = []
    for scorer in [TestScorer(), RuleScorer(), DiffScorer(), LLMJudgeScorer()]:
        trace.emit("scorer_start", f"Running {scorer.name}")
        try:
            score = scorer.score(context)
        except Exception as exc:
            errors.append(f"{scorer.name}: {exc}")
            score = ScoreResult(
                scorer_name=scorer.name,
                score=0.0,
                max_score=1.0,
                passed=False,
                evidence={"error": str(exc)},
                comments="scorer failed",
            )
        scores.append(score)
        trace.emit("scorer_finish", f"Finished {scorer.name}", score.to_dict())

    final_score = compute_final_score(scores)
    failure_taxonomy = classify_failures(scores, errors)
    status = "passed" if final_score >= 0.8 and not failure_taxonomy else "failed"
    ended_at = utc_now()

    result_json_path = run_dir / "result.json"
    report_path = run_dir / "report.md"
    artifacts = {
        "run_dir": str(run_dir),
        "workspace": str(task_dir),
        "patch_diff": str(patch_path),
        "result_json": str(result_json_path),
    }

    result = RunResult(
        run_id=actual_run_id,
        task_id=task.id,
        agent_name=agent_name,
        started_at=started_at,
        ended_at=ended_at,
        status=status,
        scores=scores,
        artifacts=artifacts,
        trace_path=str(trace_path),
        report_path=str(report_path),
        errors=errors,
        final_score=final_score,
        failure_taxonomy=failure_taxonomy,
        scenario=task.scenario,
        difficulty=task.difficulty,
        task_pack_path=str(task_pack_path),
        run_config=config.to_dict(),
    )

    write_result_json(result_json_path, result)
    write_markdown_report(report_path, result)
    trace.emit("report_generated", "Generated result.json and report.md", artifacts)
    return result


def compute_final_score(scores: list[ScoreResult]) -> float:
    weights = {
        "test": 0.45,
        "rule": 0.25,
        "diff": 0.15,
        "llm_judge": 0.15,
    }
    by_name = {score.scorer_name: score for score in scores}
    available_weights: dict[str, float] = {}
    for name, weight in weights.items():
        score = by_name.get(name)
        if score is None or score.skipped:
            continue
        available_weights[name] = weight

    total_weight = sum(available_weights.values())
    if total_weight <= 0:
        return 0.0

    weighted = 0.0
    for name, weight in available_weights.items():
        weighted += by_name[name].normalized * (weight / total_weight)
    return round(weighted, 4)


def classify_failures(scores: list[ScoreResult], errors: list[str]) -> list[str]:
    failures: set[str] = set()
    by_name = {score.scorer_name: score for score in scores}
    if errors:
        failures.add("tool_use_error")
    if by_name.get("test") and not by_name["test"].passed:
        failures.add("test_error")
        failures.add("code_error")
    if by_name.get("rule") and not by_name["rule"].passed:
        failures.add("instruction_miss")
    if by_name.get("diff") and not by_name["diff"].passed:
        failures.add("overengineering")
    if not failures and any(not score.passed and not score.skipped for score in scores):
        failures.add("incomplete_solution")
    return sorted(failures)


def load_result(path: Path) -> RunResult:
    return RunResult.from_dict(json.loads(path.read_text(encoding="utf-8")))
