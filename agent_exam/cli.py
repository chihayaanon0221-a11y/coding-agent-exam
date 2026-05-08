import argparse
from pathlib import Path

from .core.run import run_task_pack
from .reports.markdown import regenerate_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent_exam")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a local task pack")
    run_parser.add_argument("--task-pack", required=True, help="Path to a task pack directory")
    run_parser.add_argument("--agent", default="mock", help="Agent adapter name")
    run_parser.add_argument("--output-dir", default="runs", help="Directory for run artifacts")
    run_parser.add_argument("--run-id", default=None, help="Optional deterministic run id")
    run_parser.add_argument("--max-steps", type=int, default=5)
    run_parser.add_argument("--timeout-sec", type=int, default=30)

    report_parser = subparsers.add_parser("report", help="Regenerate a Markdown report")
    report_parser.add_argument("--run-id", required=True)
    report_parser.add_argument("--output-dir", default="runs")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        task_pack_paths = discover_task_packs(Path(args.task_pack))
        results = []
        for task_pack_path in task_pack_paths:
            run_id = args.run_id
            if run_id and len(task_pack_paths) > 1:
                run_id = f"{run_id}-{task_pack_path.name}"
            result = run_task_pack(
                task_pack_path=task_pack_path,
                agent_name=args.agent,
                output_dir=Path(args.output_dir),
                run_id=run_id,
                max_steps=args.max_steps,
                timeout_sec=args.timeout_sec,
            )
            results.append(result)
            print(f"Run ID: {result.run_id}")
            print(f"Result: {result.artifacts.get('result_json')}")
            print(f"Trace: {result.trace_path}")
            print(f"Report: {result.report_path}")
            print(f"Final Score: {result.final_score:.3f}")
            print(f"Status: {result.status}")
            print("")
        return 0 if all(result.status == "passed" for result in results) else 1

    if args.command == "report":
        report_path = regenerate_report(Path(args.output_dir), args.run_id)
        print(f"Report: {report_path}")
        return 0

    parser.error("unknown command")
    return 2


def discover_task_packs(path: Path) -> list[Path]:
    if (path / "task.yaml").exists():
        return [path]
    task_packs = sorted(child for child in path.iterdir() if child.is_dir() and (child / "task.yaml").exists())
    if not task_packs:
        raise FileNotFoundError(f"No task.yaml found under {path}")
    return task_packs
