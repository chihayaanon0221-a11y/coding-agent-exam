import json
import os
import urllib.parse
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OpenAICompatibleConfig:
    base_url: str
    model: str
    api_key_env: str = ""
    privacy_mode: str = "local_only"
    timeout_seconds: int = 60


def is_local_endpoint(base_url: str) -> bool:
    parsed = urllib.parse.urlparse(base_url)
    return parsed.hostname in {"127.0.0.1", "localhost", "::1"}


class OpenAICompatibleAdapter:
    name = "openai_compatible"

    def __init__(self, config: OpenAICompatibleConfig) -> None:
        if config.privacy_mode == "local_only" and not is_local_endpoint(config.base_url):
            raise ValueError("local_only mode requires localhost or loopback base_url")
        self.config = config

    def dry_run_request(self, prompt: str) -> dict[str, Any]:
        return {
            "base_url": self.config.base_url,
            "model": self.config.model,
            "privacy_mode": self.config.privacy_mode,
            "api_key_present": bool(self.config.api_key_env and os.getenv(self.config.api_key_env)),
            "prompt_chars": len(prompt),
            "dry_run": True,
        }

    def complete(self, prompt: str) -> str:
        raise NotImplementedError(
            "Real OpenAI-compatible calls are intentionally not implemented in the default harness"
        )

    def prompt_preview_json(self, prompt: str) -> str:
        return json.dumps(self.dry_run_request(prompt), sort_keys=True)

