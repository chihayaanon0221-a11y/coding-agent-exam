# Task Authoring Guide

Each exam task must be original to this repository. Public benchmarks can inform
structure, but task text and task assets must not be copied from them.

## Required Fields

- Task ID
- Task Type
- Difficulty
- Target Skills
- Baseline Path
- Allowed Files
- Forbidden Files
- Requirements
- Acceptance Criteria
- Verification Method
- Evaluation Criteria
- Privacy / Permission Notes

## Task Types

- CLI Implementation
- Bugfix
- Test Writing
- Refactoring
- Multi-file Feature
- Constraint Following
- Mini Issue Fix

## Authoring Rules

- Keep each task small enough for a personal developer to review.
- Prefer deterministic local verification commands.
- Do not require external services, databases, GPU clusters, or proprietary
  accounts for P0 tasks.
- State file boundaries clearly.
- Include privacy notes when a task could expose code, diffs, logs, or local
  configuration.
- Keep the seven constraints from `docs/codex_operating_protocol.md` central to
  every task.
