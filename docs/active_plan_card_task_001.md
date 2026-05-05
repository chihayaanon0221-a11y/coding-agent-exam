# Active Plan Card

## Task ID

task_001

## Goal

This plan card defines the future Task 001 implementation attempt: building a
small interactive TODO CLI in `baselines/task_001_todo_app/app.py`.

## Scope

Allowed files or directories:

- `baselines/task_001_todo_app/app.py`

Forbidden files or directories:

- `src/main.py`
- `exams/`
- `reports/`
- `docs/`
- repository settings
- dependency manifests or lockfiles
- credentials, secrets, tokens, or account settings

## Requirements

- Replace the current minimal JSON-output baseline with an interactive TODO CLI.
- Support `add <task title>`, `list`, `done <index>`, `delete <index>`, and `quit`.
- Keep task state in memory for the current process only.
- Use Python standard library only.
- Keep the implementation small enough for P0.

## Acceptance Criteria

Acceptance criteria are satisfied when:

- [ ] `add <task title>` stores a pending TODO item with the provided title.
- [ ] `list` prints all TODO items with 1-based indexes and done state.
- [ ] `done <index>` marks a valid item as done.
- [ ] `delete <index>` removes a valid item.
- [ ] `quit` exits cleanly with status code 0.
- [ ] Invalid commands or invalid indexes report an error and keep the CLI running.

## Verification

Commands to run:

- `python baselines/task_001_todo_app/app.py`

Expected result:

- A manual interactive session can run `add <task title>`, `list`, `done <index>`, `delete <index>`, and `quit`.
- No external dependencies are required.

## Risks

- Ambiguous command output could make manual scoring inconsistent.
- Overbuilding persistence, tests, or extra commands would exceed P0 scope.

## Agent Report Requirements

After finishing, the agent must report:

1. Files changed
2. Why each file changed
3. Commands run
4. Test results
5. Known limitations
