# Expected Behavior

`slugify(text)` should return lowercase, dash-separated text suitable for simple
URL slugs.

Examples:

- `slugify("Hello World")` returns `hello-world`
- `slugify("  Agent, Eval!  ")` returns `agent-eval`
- `slugify("")` returns an empty string

`normalize_spaces(text)` should keep collapsing repeated whitespace into single
spaces.

