# Verification Notes

## Manual Verification

Run:

```text
python baselines/task_001_todo_app/app.py
```

Then enter:

```text
list
add buy milk
list
done 1
list
delete 1
list
quit
```

Expected observations:

- The first `list` prints `No tasks.`
- The second `list` prints `1. [ ] buy milk`
- The third `list` prints `1. [x] buy milk`
- The final `list` prints `No tasks.`

## Automated Check

Run:

```text
python scripts/check_task_001.py
```

The script runs the same command sequence through `subprocess` and checks for
the required output snippets.

## Current Verification Result

PASS on the current branch:

```text
python scripts/check_task_001.py
PASS: task 001 TODO CLI behavior matched expected output
```
