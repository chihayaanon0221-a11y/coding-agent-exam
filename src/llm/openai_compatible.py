import json
import urllib.parse
from typing import Any

try:
    from .provider import ModelConfig, ModelProvider, ProviderError
except ImportError:
    from provider import ModelConfig, ModelProvider, ProviderError


def is_local_base_url(base_url: str) -> bool:
    parsed = urllib.parse.urlparse(base_url)
    return parsed.hostname in {"127.0.0.1", "localhost", "::1"}


class OpenAICompatibleProvider(ModelProvider):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__(config)
        if config.privacy_mode == "local_only" and not is_local_base_url(config.base_url):
            raise ProviderError("local_only mode requires a localhost or loopback base_url")

    def complete(self, prompt: str, *, dry_run: bool = True) -> str:
        if dry_run:
            payload: dict[str, Any] = {
                "provider": self.config.provider,
                "model": self.config.model,
                "privacy_mode": self.config.privacy_mode,
                "prompt_chars": len(prompt),
                "dry_run": True,
            }
            return json.dumps(payload, sort_keys=True)

        raise ProviderError("Real API calls are not implemented in the v0.3.0 skeleton")
