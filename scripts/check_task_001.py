import subprocess
import sys
from pathlib import Path


REQUIRED_SNIPPETS = [
    "No tasks.",
    "1. [ ] buy milk",
    "1. [x] buy milk",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    app_path = repo_root / "baselines" / "task_001_todo_app" / "app.py"

    if not app_path.exists():
        print(f"FAIL: missing app file: {app_path}")
        return 1

    input_text = "\n".join(
        [
            "list",
            "add buy milk",
            "list",
            "done 1",
            "list",
            "delete 1",
            "list",
            "quit",
            "",
        ]
    )

    try:
        completed = subprocess.run(
            [sys.executable, str(app_path)],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=10,
            cwd=repo_root,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print("FAIL: task 001 app timed out")
        return 1

    output = completed.stdout + completed.stderr

    if completed.returncode != 0:
        print(f"FAIL: app exited with code {completed.returncode}")
        print(output)
        return 1

    missing = [snippet for snippet in REQUIRED_SNIPPETS if snippet not in output]
    if missing:
        print("FAIL: missing expected output")
        for snippet in missing:
            print(f"- {snippet}")
        print("Captured output:")
        print(output)
        return 1

    print("PASS: task 001 TODO CLI behavior matched expected output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
