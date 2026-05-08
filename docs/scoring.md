# Scoring

The harness follows a transparent, multi-dimensional scoring model inspired by
OpenAI Evals, HELM, lm-evaluation-harness, SWE-bench, and agent task benchmarks.

## Metrics

Reports expose these dimensions:

- correctness
- test_pass
- instruction_following
- code_quality
- diff_minimality
- robustness
- reproducibility

The current implementation maps these to concrete scorers:

- `TestScorer`: correctness and test_pass
- `RuleScorer`: instruction_following and reproducibility
- `DiffScorer`: diff_minimality and code_quality proxy
- `LLMJudgeScorer`: optional qualitative scorer, skipped by default

## Score Formula

Default final score:

```text
0.45 * test_score
+ 0.25 * rule_score
+ 0.15 * diff_score
+ 0.15 * judge_score_if_available
```

If the judge scorer is skipped, the available deterministic scorer weights are
renormalized.

## Failure Taxonomy

Reports can include:

- planning_error
- tool_use_error
- code_error
- test_error
- instruction_miss
- overengineering
- incomplete_solution

The current runner infers common failures from scorer outcomes. Richer trace
analysis is a future extension.

## LLM Judge Policy

LLM judging is optional and cannot replace tests or rules. Any future judge must:

- cite evidence
- score each dimension separately
- avoid rewarding verbosity
- ignore model names
- output JSON

