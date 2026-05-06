from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    base_url: str
    model: str
    api_key_env: str
    privacy_mode: str
    timeout_seconds: int
    notes: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ModelConfig":
        return cls(
            provider=str(data["provider"]),
            base_url=str(data["base_url"]),
            model=str(data["model"]),
            api_key_env=str(data.get("api_key_env", "")),
            privacy_mode=str(data["privacy_mode"]),
            timeout_seconds=int(data.get("timeout_seconds", 60)),
            notes=str(data.get("notes", "")),
        )


class ProviderError(Exception):
    pass


class ModelProvider:
    def __init__(self, config: ModelConfig) -> None:
        self.config = config

    def complete(self, prompt: str, *, dry_run: bool = True) -> str:
        raise NotImplementedError
