# Architecture

## Project Positioning

`coding-agent-exam` is a Personal Developer Coding Agent Harness.

It is built for local personal-developer workflows: a developer has a repository,
a constrained task, a baseline, a model configuration, a verification command,
Git evidence, and an attempt report.

This project is not a general benchmark leaderboard. It is not intended to
compete directly with large benchmark suites. It focuses on whether a coding
agent can complete practical local tasks while respecting boundaries that matter
to an individual developer.

## System Components

- Task specs: Markdown files in `exams/` that define goals, constraints,
  deliverables, and evaluation criteria.
- Baselines: small starter projects in `baselines/` that future agents modify.
- Constraints: the seven operating constraints in
  `docs/codex_operating_protocol.md`.
- Model provider config: local-first configuration examples in `config/`.
- Execution shell / future agent shell: lightweight Python entry points that can
  later orchestrate task loading, provider selection, and command execution.
- Verification scripts: standard-library scripts in `scripts/` that check
  behavior without requiring cloud services.
- Attempt records: reproducible records in `attempts/` containing reports,
  verification notes, and diffs.
- Reports: templates and human-readable summaries in `reports/`.

## Central Constraints

Every harness task should preserve these constraints:

- Goal Constraint
- Plan Card Constraint
- File Boundary Constraint
- Git Constraint
- Verification Constraint
- Permission Constraint
- Review Gate Constraint

## Codex vs Internal Agent Shell

Codex is an external developer working on this repository. Codex edits files,
runs checks, commits changes, and produces reports.

The project internal agent shell is future product code inside this repository.
It should eventually help run local coding-agent attempts, load model provider
configuration, execute verification scripts, and record attempt artifacts.

These roles must stay separate. Codex can improve the harness, but Codex is not
the harness runtime itself.

## P0 Does

- Define original local coding-agent tasks.
- Keep task scopes small and reviewable.
- Use local baselines and local verification scripts.
- Record Git diffs and attempt reports.
- Provide privacy-first model configuration.
- Keep model providers hot-swappable at the configuration and interface level.

## P0 Does Not

- Provide a public leaderboard.
- Run a complex LLM judge agent.
- Depend on MCP, plugins, third-party agent frameworks, cloud databases, or GPU
  clusters.
- Upload repository content to cloud services.
- Run multi-model large-scale benchmarks.
- Create a Web UI.

## v0.3.0 Boundary

`v0.3.0` establishes the harness foundation:

- Personal developer first.
- Local-first and privacy-first by default.
- Standard-library-only tooling.
- OpenAI-compatible local provider skeleton.
- Expandable task catalog.
- Task 001 verification script and attempt record layout.

It does not implement a full autonomous coding agent.

## Future Roadmap

- Add a small local agent shell that can load one task and one provider config.
- Add more baseline projects for the task catalog.
- Add deterministic verification scripts for each task.
- Add optional remote API support that requires explicit user configuration.
- Add report generation from Git status, diff, and verification results.
- Explore a judge-agent workflow later, after local evidence collection is
  stable.
