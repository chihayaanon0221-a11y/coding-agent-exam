# Git Workflow



## Branch Rules



- main is the stable branch.

- Each agent attempt should use a separate branch.

- Branch name format:



agent/task-XXX-agent-name



Example:



agent/task-001-codex



## Commit Rules



Each task should produce a small number of reviewable commits.



Commit message format:



task-XXX: short summary



Example:



task-001: implement todo cli commands



## Before Commit



The agent should run:



- git status

- git diff



## After Commit



The agent should record:



- git log --oneline -5

- git diff main...HEAD



## Forbidden Operations



Agents should not:



- force push

- push directly to main

- delete branches

- change repository settings

- edit secrets or credentials



