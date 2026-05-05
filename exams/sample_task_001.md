# Task 001: TODO CLI

## Background

The baseline project in `baselines/task_001_todo_app/` currently contains a
minimal Python script. This exam asks a coding agent to turn that baseline into a
small interactive TODO command-line application.

For `v0.1.3`, this file defines the first real coding-agent exam task. The
future solution should stay small, reviewable, and limited to P0 scope.

## Goal

Modify `baselines/task_001_todo_app/app.py` so it runs an interactive TODO CLI.
The CLI should keep TODO items in memory for the current process and support
`add <task title>`, `list`, `done <index>`, `delete <index>`, and `quit`.

## Requirements

- Support `add <task title>`.
  - Add a new pending TODO item using the full text after `add`.
  - Reject empty task titles with an error message.
- Support `list`.
  - Print all TODO items with 1-based indexes.
  - Show pending items as `[ ]` and done items as `[x]`.
  - Print `No tasks.` when the list is empty.
- Support `done <index>`.
  - Mark the TODO item at the 1-based index as done.
  - Report an error for missing, non-numeric, or out-of-range indexes.
- Support `delete <index>`.
  - Remove the TODO item at the 1-based index.
  - Report an error for missing, non-numeric, or out-of-range indexes.
- Support `quit`.
  - Quit cleanly with status code 0.
- For any unknown command, print an error and continue running.

## Constraints

- Modify only `baselines/task_001_todo_app/app.py`.
- Do not modify `src/main.py`.
- Do not modify `exams/`, `docs/`, or `reports/` while solving the exam task.
- Do not add external dependencies.
- Use Python standard library only.
- Keep state in memory only; do not add file persistence.
- Keep the implementation small enough for P0.
- Do not commit, push, force push, or change repository settings unless
  explicitly instructed.

## Expected Deliverables

- Updated `baselines/task_001_todo_app/app.py`.
- A short completion report that includes:
  1. Files changed
  2. Why each file changed
  3. Commands run
  4. Verification result
  5. Known limitations

## Evaluation Criteria

- Correctness: all five commands behave as specified.
- Simplicity: the implementation stays small and avoids unnecessary features.
- Readability: command parsing and TODO state handling are easy to follow.
- Error handling: invalid commands and indexes are handled without crashing.
- Testability: behavior can be verified through a clear manual CLI session.
- Constraint following: only allowed files are changed and no dependencies are added.
- Git hygiene: status, diff, and verification results are reported clearly.
