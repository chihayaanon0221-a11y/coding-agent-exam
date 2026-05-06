# Coding Agent Exam

A lightweight local harness for testing coding agents on constrained personal
developer tasks.

## Goal

This project explores how coding agents perform in exam-like coding scenarios
inside a local developer repository.

The current direction is a Personal Developer Coding Agent Harness: task specs,
baselines, constraints, local verification scripts, Git evidence, attempt
records, and reports.

## P0 Scope

- Create small original coding tasks
- Provide local baseline projects
- Run coding agent attempts
- Record git diff and commit evidence
- Run local verification scripts
- Produce manual score reports

## Current Status

`v0.3.0` establishes the local harness foundation. The project now has a Task
001 TODO CLI exam, a local verification script, privacy-first model config
example, and an expandable task catalog.

## Personal Developer Harness Direction

This project is not a public leaderboard or large cloud benchmark. It is focused
on personal developer workflows:

- local repositories
- explicit task constraints
- Git diff evidence
- standard-library verification scripts
- attempt reports
- future hot-swappable model providers

The seven constraints in `docs/codex_operating_protocol.md` remain central.

## How to Run Task 001 Check

```text
python scripts/check_task_001.py
```

The checker runs `baselines/task_001_todo_app/app.py` through a short TODO CLI
session and expects `No tasks.`, `1. [ ] buy milk`, and `1. [x] buy milk`.

## Privacy-First Model Config

See `config/model.example.json`.

The default recommended mode is `local_only`, using a localhost or loopback
OpenAI-compatible endpoint such as `http://127.0.0.1:11434/v1`.

Remote API usage must be explicit with `remote_api_allowed`. Repository content,
credentials, secrets, tokens, and account settings must not be uploaded by
default.

## Current Limitations

- No full autonomous agent shell yet.
- No complex judge agent.
- No Web UI, database, leaderboard, or cloud runner.
- Provider code is a lightweight skeleton and does not make real API calls.
