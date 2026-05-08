from agent_exam.core.result import ScoreResult
from agent_exam.scorers.base import Scorer, ScoringContext
from agent_exam.utils.subprocess_utils import run_command


class TestScorer(Scorer):
    name = "test"

    def score(self, context: ScoringContext) -> ScoreResult:
        command = str(context.task.scoring_profile.get("test_command", "")).strip()
        if not command:
            return ScoreResult(
                scorer_name=self.name,
                score=0.0,
                max_score=1.0,
                passed=False,
                evidence={"skipped": True},
                comments="No test_command configured.",
            )

        result = run_command(command, context.task_dir, timeout_sec=60)
        output_path = context.run_dir / "test_output.txt"
        output_path.write_text(result.combined_output, encoding="utf-8")
        passed = result.returncode == 0
        return ScoreResult(
            scorer_name=self.name,
            score=1.0 if passed else 0.0,
            max_score=1.0,
            passed=passed,
            evidence={
                "command": command,
                "cwd": str(context.task_dir),
                "returncode": result.returncode,
                "output_path": str(output_path),
            },
            comments="Tests passed." if passed else "Tests failed.",
        )
