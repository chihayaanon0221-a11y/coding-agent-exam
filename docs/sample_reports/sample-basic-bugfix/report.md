# Agent Evaluation Report

## Summary

- Agent: `mock`
- Task Pack: `examples\task_packs\basic_bugfix`
- Run ID: `sample-basic-bugfix`
- Final Score: `1.000`
- Pass/Fail: `passed`

## Task Results

| task_id | scenario | difficulty | status | final_score | test_score | rule_score | diff_score | judge_score |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| basic_bugfix | bugfix | easy | passed | 1.000 | 1.000 | 1.000 | 1.000 | skipped |

## Metrics

- correctness: covered by test_score
- test_pass: covered by test_score
- instruction_following: covered by rule_score
- code_quality: approximated by rule and diff evidence
- diff_minimality: covered by diff_score
- robustness: covered by task tests and rule checks
- reproducibility: covered by trace, result, report, and commands

## Failure Analysis

- none

## Evidence

- Changed files: `calculator.py`
- Test output path: `runs\sample-basic-bugfix\test_output.txt`
- Trace path: `runs\sample-basic-bugfix\trace.jsonl`
- Artifact path: `runs\sample-basic-bugfix`

## Scorer Details

### test

- Score: `1.0/1.0`
- Passed: `True`
- Comments: Tests passed.
- Evidence: `{'command': 'python -m unittest discover tests', 'cwd': 'runs\\sample-basic-bugfix\\workspace', 'returncode': 0, 'output_path': 'runs\\sample-basic-bugfix\\test_output.txt'}`

### rule

- Score: `1.0/1.0`
- Passed: `True`
- Comments: 4/4 rule checks passed.
- Evidence: `{'checks': [{'name': 'required file exists: repo/calculator.py', 'passed': True}, {'name': 'forbidden file absent: repo/credentials.txt', 'passed': True}, {'name': 'required text in repo\\calculator.py: return a + b', 'passed': True}, {'name': 'forbidden text absent in repo\\calculator.py: requests', 'passed': True}]}`

### diff

- Score: `1.0/1.0`
- Passed: `True`
- Comments: Diff size is within the configured limit.
- Evidence: `{'original_repo': 'examples\\task_packs\\basic_bugfix\\repo', 'working_repo': 'runs\\sample-basic-bugfix\\workspace\\repo', 'diff_lines': 4, 'max_diff_lines': 20, 'changed_files': ['calculator.py']}`

### llm_judge

- Score: `skipped`
- Passed: `True`
- Comments: Optional LLM judge skipped.
- Evidence: `{'skipped': True, 'reason': 'AGENT_EXAM_JUDGE_API_KEY is not set'}`

## Reproducibility

```text
python -m agent_exam run --task-pack examples\task_packs\basic_bugfix
python -m agent_exam report --run-id sample-basic-bugfix
```
