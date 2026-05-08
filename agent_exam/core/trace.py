import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class TraceEvent:
    timestamp: str
    event_type: str
    task_id: str
    step: int
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TraceWriter:
    def __init__(self, path: Path, task_id: str) -> None:
        self.path = path
        self.task_id = task_id
        self.step = 0
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event_type: str, message: str, metadata: dict[str, Any] | None = None) -> None:
        self.step += 1
        event = TraceEvent(
            timestamp=utc_now(),
            event_type=event_type,
            task_id=self.task_id,
            step=self.step,
            message=message,
            metadata=metadata or {},
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")

