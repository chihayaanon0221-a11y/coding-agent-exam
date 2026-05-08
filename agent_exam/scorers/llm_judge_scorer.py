import os

from agent_exam.core.result import ScoreResult
from agent_exam.scorers.base import Scorer, ScoringContext


JUDGE_PROMPT_TEMPLATE = """You are an impartial coding-agent evaluation judge.
Return JSON only.
Evaluate each dimension separately: correctness, instruction_following,
code_quality, diff_minimality, robustness, reproducibility.
Use evidence from the task, diff, tests, and report. Do not reward verbosity.
Do not prefer or penalize any model name.
"""


class LLMJudgeScorer(Scorer):
    name = "llm_judge"

    def score(self, context: ScoringContext) -> ScoreResult:
        api_key = os.getenv("AGENT_EXAM_JUDGE_API_KEY")
        if not api_key:
            return ScoreResult(
                scorer_name=self.name,
                score=0.0,
                max_score=1.0,
                passed=True,
                evidence={"skipped": True, "reason": "AGENT_EXAM_JUDGE_API_KEY is not set"},
                comments="Optional LLM judge skipped.",
            )

        return ScoreResult(
            scorer_name=self.name,
            score=0.0,
            max_score=1.0,
            passed=False,
            evidence={
                "skipped": True,
                "reason": "LLM judge API execution is not implemented",
                "prompt_template": JUDGE_PROMPT_TEMPLATE,
            },
            comments="LLM judge is an optional interface skeleton.",
        )

