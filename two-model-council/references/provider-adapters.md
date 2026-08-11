# Provider adapters

Built in: `claude`, `codex`, and `gemini`. Select with `--provider`; `--peer`
remains a backward-compatible alias.

For another CLI, pass `--adapter-config providers.json`. Prompts are sent on stdin,
and commands are executed as argument arrays without a shell.

```json
{
  "providers": {
    "kimi": {
      "command": ["kimi", "--print"],
      "readOnlyArgs": ["--permission-mode", "plan"],
      "modelArgs": ["--model", "{model}"],
      "effortArgs": ["--effort", "{effort}"],
      "budgetArgs": [],
      "outputFormat": "text"
    },
    "ollama": {
      "command": ["ollama", "run"],
      "readOnlyArgs": [],
      "modelArgs": ["{model}"],
      "effortArgs": [],
      "budgetArgs": [],
      "outputFormat": "text"
    }
  }
}
```

Verify every adapter against the installed CLI version. For hosted products,
keep the registry server-owned and allowlisted. Never accept arbitrary command
configuration from end users or place credentials in the adapter file.
