# Codex Operating Protocol

This protocol is the primary operating guide for Codex work in this repository.
It applies to every task unless the user gives a narrower instruction.

## 1. Goal Constraint

- Every task must state exactly what task ID, version, or project milestone it advances.
- The agent must keep the work scoped to that stated goal.
- The agent must not expand scope, add adjacent features, or perform opportunistic cleanup without explicit permission.

## 2. Plan Card Constraint

- Every task must have an active plan card before editing begins.
- The agent must read the active plan card before editing.
- If no active plan card exists, the agent must stop and ask for one, or create one only when explicitly allowed.
- The plan card should follow `docs/plan_card_template.md`.

## 3. File Boundary Constraint

- The active plan card must list allowed files or directories.
- The active plan card must list forbidden files or directories.
- The agent must not modify forbidden files.
- If a required change falls outside the allowed boundary, the agent must stop and request permission before editing.

## 4. Git Constraint

- Work should happen on a task branch, not directly on `main`.
- The agent must not push to `main`.
- The agent must not force push.
- The agent must not change repository settings, delete branches, or rewrite shared history.
- Before reporting completion, the agent must run:
  - `git status`
  - `git diff`
- The agent must not commit unless explicitly asked to commit.

## 5. Verification Constraint

- The agent must run relevant checks for the task.
- If no automated check exists, the agent must explain why and provide the best available manual verification.
- The agent must report the exact commands run and the observed results.
- Verification should be scoped to the files and behavior changed by the task.

## 6. Permission Constraint

- The agent must not request broad access unless it is necessary for the task.
- The preferred execution mode is `workspace-write` with `on-request` approval.
- The agent must not touch credentials, secrets, tokens, account settings, or external service configuration.
- The agent must not add dependencies unless the task explicitly authorizes them.

## 7. Review Gate Constraint

- The agent's work is not complete until a human reviews the diff.
- The agent must report:
  1. Files changed
  2. Why each file changed
  3. Commands run
  4. Verification result
  5. Known limitations
- The final report must make clear whether human review is still pending.

