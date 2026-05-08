# Agent Evaluation Report

## Summary

- Agent: `mock`
- Task Pack: `examples\task_packs\feature_addition`
- Run ID: `sample-feature-addition`
- Final Score: `1.000`
- Pass/Fail: `passed`

## Task Results

| task_id | scenario | difficulty | status | final_score | test_score | rule_score | diff_score | judge_score |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| feature_addition | multi-file feature | easy | passed | 1.000 | 1.000 | 1.000 | 1.000 | skipped |

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

- Changed files: `text_utils.py`
- Test output path: `runs\sample-feature-addition\test_output.txt`
- Trace path: `runs\sample-feature-addition\trace.jsonl`
- Artifact path: `runs\sample-feature-addition`

## Scorer Details

### test

- Score: `1.0/1.0`
- Passed: `True`
- Comments: Tests passed.
- Evidence: `{'command': 'python -m unittest discover tests', 'cwd': 'runs\\sample-feature-addition\\workspace', 'returncode': 0, 'output_path': 'runs\\sample-feature-addition\\test_output.txt'}`

### rule

- Score: `1.0/1.0`
- Passed: `True`
- Comments: 4/4 rule checks passed.
- Evidence: `{'checks': [{'name': 'required file exists: repo/text_utils.py', 'passed': True}, {'name': 'forbidden file absent: repo/secrets.json', 'passed': True}, {'name': 'required text in repo\\text_utils.py: def slugify', 'passed': True}, {'name': 'forbidden text absent in repo\\text_utils.py: import requests', 'passed': True}]}`

### diff

- Score: `1.0/1.0`
- Passed: `True`
- Comments: Diff size is within the configured limit.
- Evidence: `{'original_repo': 'examples\\task_packs\\feature_addition\\repo', 'working_repo': 'runs\\sample-feature-addition\\workspace\\repo', 'diff_lines': 14, 'max_diff_lines': 80, 'changed_files': ['text_utils.py']}`

### llm_judge

- Score: `skipped`
- Passed: `True`
- Comments: Optional LLM judge skipped.
- Evidence: `{'skipped': True, 'reason': 'AGENT_EXAM_JUDGE_API_KEY is not set'}`

## Reproducibility

```text
python -m agent_exam run --task-pack examples\task_packs\feature_addition
python -m agent_exam report --run-id sample-feature-addition
```
