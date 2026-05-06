# Privacy Model

## Default Mode: `local_only`

The recommended default privacy mode is `local_only`.

In `local_only` mode, repository code, prompts, task context, diffs, reports, and
verification output should remain on the user's machine. Model endpoints should
use localhost addresses such as:

- `http://127.0.0.1:11434/v1`
- `http://localhost:11434/v1`

The harness should reject or warn on non-local endpoints when privacy mode is
`local_only`.

## Remote Mode: `remote_api_allowed`

`remote_api_allowed` means the user explicitly permits calls to a remote model
API. This mode must be configured intentionally.

Any endpoint that is not localhost or loopback counts as remote API usage,
including hosted model APIs, cloud inference gateways, and company-internal
network services outside the local machine.

Remote API mode must not be assumed from the provider name alone. The user must
set the privacy mode and endpoint deliberately, and must explicitly confirm that
remote API use is acceptable for the task.

## Information That Must Not Be Uploaded

The harness must not upload or transmit:

- credentials
- secrets
- tokens
- account settings
- private keys
- environment files containing sensitive data
- repository content unless remote API mode is explicitly configured

## Credentials and Account Settings

The harness must not read, write, rotate, or manage credentials, secrets, tokens,
or account settings.

Configuration may name an environment variable such as `LOCAL_LLM_API_KEY`, but
the harness should not print its value or persist it into reports.
