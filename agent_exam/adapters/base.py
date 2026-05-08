from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from agent_exam.core.task import TaskSpec


class AgentAdapter(ABC):
    name = "base"

    @abstractmethod
    def run(self, task: TaskSpec, task_dir: Path) -> dict[str, Any]:
        raise NotImplementedError

