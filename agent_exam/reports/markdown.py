from pathlib import Path

from agent_exam.core.result import RunResult


def write_markdown_report(path: Path, result: RunResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(result), encoding="utf-8")


def regenerate_report(output_dir: Path, run_id: str) -> Path:
    from agent_exam.core.run import load_result

    result_path = output_dir / run_id / "result.json"
    result = load_result(result_path)
    report_path = output_dir / run_id / "report.md"
    write_markdown_report(report_path, result)
    return report_path


def render_markdown_report(result: RunResult) -> str:
    score_lookup = {score.scorer_name: score for score in result.scores}
    judge_score = _fmt_score(score_lookup.get("llm_judge"))
    lines = [
        "# Agent Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Agent: `{result.agent_name}`",
        f"- Task Pack: `{result.task_pack_path}`",
        f"- Run ID: `{result.run_id}`",
        f"- Final Score: `{result.final_score:.3f}`",
        f"- Pass/Fail: `{result.status}`",
        "",
        "## Task Results",
        "",
        "| task_id | scenario | difficulty | status | final_score | test_score | rule_score | diff_score | judge_score |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| {result.task_id} | {result.scenario} | {result.difficulty} | {result.status} | "
            f"{result.final_score:.3f} | {_fmt_score(score_lookup.get('test'))} | "
            f"{_fmt_score(score_lookup.get('rule'))} | {_fmt_score(score_lookup.get('diff'))} | "
            f"{judge_score} |"
        ),
        "",
        "## Metrics",
        "",
        "- correctness: covered by test_score",
        "- test_pass: covered by test_score",
        "- instruction_following: covered by rule_score",
        "- code_quality: approximated by rule and diff evidence",
        "- diff_minimality: covered by diff_score",
        "- robustness: covered by task tests and rule checks",
        "- reproducibility: covered by trace, result, report, and commands",
        "",
        "## Failure Analysis",
        "",
    ]

    if result.failure_taxonomy:
        lines.extend(f"- {item}" for item in result.failure_taxonomy)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- Changed files: `{_changed_files(result)}`",
            f"- Test output path: `{_score_evidence(result, 'test', 'output_path')}`",
            f"- Trace path: `{result.trace_path}`",
            f"- Artifact path: `{result.artifacts.get('run_dir', '')}`",
            "",
            "## Scorer Details",
            "",
        ]
    )

    for score in result.scores:
        lines.extend(
            [
                f"### {score.scorer_name}",
                "",
                f"- Score: `{_score_detail(score)}`",
                f"- Passed: `{score.passed}`",
                f"- Comments: {score.comments}",
                f"- Evidence: `{score.evidence}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Reproducibility",
            "",
            "```text",
            f"python -m agent_exam run --task-pack {result.task_pack_path}",
            f"python -m agent_exam report --run-id {result.run_id}",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def _fmt_score(value) -> str:
    if value is None:
        return "n/a"
    if value.skipped:
        return "skipped"
    return f"{value.normalized:.3f}"


def _score_evidence(result: RunResult, scorer_name: str, key: str) -> str:
    for score in result.scores:
        if score.scorer_name == scorer_name:
            return str(score.evidence.get(key, ""))
    return ""


def _changed_files(result: RunResult) -> str:
    for score in result.scores:
        if score.scorer_name == "diff":
            return ", ".join(score.evidence.get("changed_files", []))
    return ""


def _score_detail(score) -> str:
    if score.skipped:
        return "skipped"
    return f"{score.score}/{score.max_score}"
