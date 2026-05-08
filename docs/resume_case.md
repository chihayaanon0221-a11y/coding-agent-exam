# Resume Case Study

## Project Background

This project is a lightweight evaluation framework prototype for Coding Agents
in a local personal-developer setting. The goal is to make sample agent runs
reproducible and inspectable without relying on a cloud benchmark platform.

## Technical Challenges

- Designing a minimal task schema without adding parsing dependencies.
- Capturing useful run evidence: trace, patch diff, test output, scores, and
  reports.
- Separating deterministic scoring from optional LLM-as-judge evaluation.
- Keeping examples small enough to run locally while still resembling real
  engineering tasks.

## Solution

- Built a standard-library CLI harness with task loading, run workspaces, mock
  agent execution, scorers, trace logging, and report generation.
- Added two runnable toy repo task packs: bugfix and feature addition.
- Implemented test, rule, and diff scoring before optional judge scoring.
- Generated Markdown and JSON reports with failure taxonomy and reproduction
  commands.

## Quantified Result

- Two sample task packs run locally end to end.
- Each run generates five artifacts: `result.json`, `trace.jsonl`, `report.md`,
  `patch.diff`, and `test_output.txt`.
- Project tests validate task loading and report generation.

## Resume Bullets

- Designed and implemented a lightweight Coding Agent evaluation framework
  prototype with task definitions, execution traces, multi-dimensional scoring, and
  Markdown/JSON report generation.
- Built reproducible toy repo engineering tasks using standard-library tests,
  rule checks, and diff analysis to evaluate agent code modifications.
- Adapted ideas from OpenAI Evals, HELM, SWE-bench, and lm-evaluation-harness
  into a local-first prototype with `TaskSpec`, `Scorer`, `Runner`, and report
  abstractions.
