#!/usr/bin/env python3
"""Run a configured model provider non-interactively and save its visible answer."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider",
        "--peer",
        dest="provider",
        required=True,
        help="Built-in provider (claude, codex, gemini) or an adapter-config provider name.",
    )
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument(
        "--model",
        help="Model or provider alias for this peer call. Omit to inherit the CLI default.",
    )
    parser.add_argument(
        "--effort",
        help="Reasoning effort for this peer call, such as low, medium, or high.",
    )
    parser.add_argument(
        "--max-budget-usd",
        type=float,
        help="Provider budget ceiling when its adapter supports one.",
    )
    parser.add_argument(
        "--adapter-config",
        type=Path,
        help="JSON registry for additional CLI providers such as Kimi or Ollama.",
    )
    parser.add_argument(
        "--source-file",
        action="append",
        default=[],
        type=Path,
        help="Attach an exact local file to the prompt. Repeat for multiple files.",
    )
    parser.add_argument(
        "--allow-workspace-read",
        action="store_true",
        help="Allow the peer to read and search files under --cwd; never enables writes or shell tools.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=300,
        help="Peer response timeout. Defaults to 300 seconds.",
    )
    return parser.parse_args()


def run_claude(
    prompt: str,
    cwd: Path,
    allow_workspace_read: bool,
    timeout_seconds: int,
    model: str | None,
    effort: str | None,
    max_budget_usd: float | None,
) -> str:
    auth = subprocess.run(
        ["claude", "auth", "status"],
        text=True,
        capture_output=True,
        cwd=cwd,
        check=False,
        timeout=15,
    )
    try:
        auth_payload = json.loads(auth.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Could not determine Claude CLI authentication status") from exc
    if not auth_payload.get("loggedIn"):
        raise RuntimeError("Claude CLI is not authenticated; run `claude auth login` interactively")

    command = [
        "claude",
        "-p",
        "--permission-mode",
        "dontAsk",
        "--tools",
        "Read,Glob,Grep" if allow_workspace_read else "",
        "--output-format",
        "json",
        "--max-turns",
        "6",
    ]
    if model:
        command.extend(["--model", model])
    if effort:
        command.extend(["--effort", effort])
    if max_budget_usd is not None:
        command.extend(["--max-budget-usd", str(max_budget_usd)])
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        cwd=cwd,
        check=False,
        timeout=timeout_seconds,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Claude exited without an error message")
    payload = json.loads(completed.stdout)
    result = payload.get("result")
    if not isinstance(result, str) or not result.strip():
        raise RuntimeError("Claude returned no visible result")
    visible = result.strip()
    marker = "## Claude —"
    marker_index = visible.rfind(marker)
    if marker_index >= 0:
        visible = visible[marker_index:]
    return visible + "\n"


def run_codex(
    prompt: str,
    cwd: Path,
    allow_workspace_read: bool,
    timeout_seconds: int,
    model: str | None,
    effort: str | None,
) -> str:
    if allow_workspace_read:
        run_dir = str(cwd)
        temporary_dir = None
    else:
        temporary_dir = tempfile.TemporaryDirectory(prefix="two-model-council-")
        run_dir = temporary_dir.name
    try:
        command = ["codex", "exec"]
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["--config", f'model_reasoning_effort="{effort}"'])
        command.extend([
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--color",
            "never",
            "-C",
            run_dir,
            "-",
        ])
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            cwd=run_dir,
            check=False,
            timeout=timeout_seconds,
        )
    finally:
        if temporary_dir is not None:
            temporary_dir.cleanup()
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Codex exited without an error message")
    if not completed.stdout.strip():
        raise RuntimeError("Codex returned no visible result")
    return completed.stdout.strip() + "\n"


def run_gemini(
    prompt: str,
    cwd: Path,
    allow_workspace_read: bool,
    timeout_seconds: int,
    model: str | None,
    effort: str | None,
    max_budget_usd: float | None,
) -> str:
    if effort:
        raise RuntimeError("Gemini CLI does not expose a reasoning-effort flag")
    if max_budget_usd is not None:
        raise RuntimeError("Gemini CLI does not expose a per-call USD budget flag")
    if allow_workspace_read:
        run_dir = str(cwd)
        temporary_dir = None
    else:
        temporary_dir = tempfile.TemporaryDirectory(prefix="two-model-council-")
        run_dir = temporary_dir.name
    try:
        command = [
            "gemini",
            "--approval-mode",
            "plan",
            "--output-format",
            "json",
            "--prompt",
            prompt,
        ]
        if model:
            command.extend(["--model", model])
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            cwd=run_dir,
            check=False,
            timeout=timeout_seconds,
        )
    finally:
        if temporary_dir is not None:
            temporary_dir.cleanup()
    if completed.returncode != 0:
        try:
            error_payload = json.loads(completed.stdout)
            message = error_payload.get("error", {}).get("message")
        except (json.JSONDecodeError, AttributeError):
            message = None
        raise RuntimeError(message or completed.stderr.strip() or "Gemini failed")
    payload = json.loads(completed.stdout)
    result = payload.get("response") or payload.get("result") or payload.get("text")
    if not isinstance(result, str) or not result.strip():
        raise RuntimeError("Gemini returned no visible result")
    return result.strip() + "\n"


def _render_adapter_args(template: object, value: str, field: str) -> list[str]:
    if not isinstance(template, list) or not all(isinstance(item, str) for item in template):
        raise RuntimeError(f"Adapter {field} must be an array of strings")
    return [item.replace("{" + field + "}", value) for item in template]


def run_external(
    provider: str,
    adapter_config: Path,
    prompt: str,
    cwd: Path,
    allow_workspace_read: bool,
    timeout_seconds: int,
    model: str | None,
    effort: str | None,
    max_budget_usd: float | None,
) -> str:
    if not adapter_config.is_file():
        raise RuntimeError(f"Adapter config does not exist: {adapter_config}")
    registry = json.loads(adapter_config.read_text(encoding="utf-8"))
    providers = registry.get("providers")
    adapter = providers.get(provider) if isinstance(providers, dict) else None
    if not isinstance(adapter, dict):
        raise RuntimeError(f"Provider is not defined in adapter config: {provider}")
    command = adapter.get("command")
    if not isinstance(command, list) or not command or not all(
        isinstance(item, str) and item for item in command
    ):
        raise RuntimeError("Adapter command must be a non-empty array of strings")
    argv = list(command)
    read_only_args = adapter.get("readOnlyArgs", [])
    if not isinstance(read_only_args, list) or not all(
        isinstance(item, str) for item in read_only_args
    ):
        raise RuntimeError("Adapter readOnlyArgs must be an array of strings")
    argv.extend(read_only_args)
    if model:
        argv.extend(_render_adapter_args(adapter.get("modelArgs", []), model, "model"))
    if effort:
        argv.extend(_render_adapter_args(adapter.get("effortArgs", []), effort, "effort"))
    if max_budget_usd is not None:
        argv.extend(
            _render_adapter_args(
                adapter.get("budgetArgs", []), str(max_budget_usd), "budget"
            )
        )
    if allow_workspace_read:
        run_dir = str(cwd)
        temporary_dir = None
    else:
        temporary_dir = tempfile.TemporaryDirectory(prefix="two-model-council-")
        run_dir = temporary_dir.name
    try:
        completed = subprocess.run(
            argv,
            input=prompt,
            text=True,
            capture_output=True,
            cwd=run_dir,
            check=False,
            timeout=timeout_seconds,
        )
    finally:
        if temporary_dir is not None:
            temporary_dir.cleanup()
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"{provider} failed")
    output_format = adapter.get("outputFormat", "text")
    if output_format == "text":
        result = completed.stdout
    elif output_format == "json":
        payload = json.loads(completed.stdout)
        result_field = adapter.get("resultField", "result")
        result = payload.get(result_field) if isinstance(payload, dict) else None
    else:
        raise RuntimeError("Adapter outputFormat must be text or json")
    if not isinstance(result, str) or not result.strip():
        raise RuntimeError(f"{provider} returned no visible result")
    return result.strip() + "\n"


def main() -> int:
    args = parse_args()
    cwd = args.cwd.resolve()
    prompt_path = args.prompt.resolve()
    output_path = args.output.resolve()
    if not cwd.is_dir():
        raise RuntimeError(f"Working directory does not exist: {cwd}")
    if not prompt_path.is_file():
        raise RuntimeError(f"Prompt file does not exist: {prompt_path}")
    if output_path == prompt_path:
        raise RuntimeError("Prompt and output paths must differ")

    prompt = prompt_path.read_text(encoding="utf-8")
    if args.source_file:
        sections = [prompt.rstrip(), "\n\n# Authorized source packet"]
        for requested_source in args.source_file:
            source_path = requested_source.resolve()
            if not source_path.is_file():
                raise RuntimeError(f"Source file does not exist: {source_path}")
            try:
                display_path = source_path.relative_to(cwd)
            except ValueError as exc:
                raise RuntimeError(
                    f"Source file must be inside --cwd: {source_path}"
                ) from exc
            sections.extend(
                [
                    f"\n\n## SOURCE: {display_path.as_posix()}\n",
                    source_path.read_text(encoding="utf-8"),
                ]
            )
        prompt = "".join(sections)
    if args.provider == "claude":
        answer = run_claude(
            prompt,
            cwd,
            args.allow_workspace_read,
            args.timeout_seconds,
            args.model,
            args.effort,
            args.max_budget_usd,
        )
    elif args.provider == "codex":
        if args.max_budget_usd is not None:
            raise RuntimeError("Codex CLI does not expose a per-call USD budget flag")
        answer = run_codex(
            prompt,
            cwd,
            args.allow_workspace_read,
            args.timeout_seconds,
            args.model,
            args.effort,
        )
    elif args.provider == "gemini":
        answer = run_gemini(
            prompt,
            cwd,
            args.allow_workspace_read,
            args.timeout_seconds,
            args.model,
            args.effort,
            args.max_budget_usd,
        )
    elif args.adapter_config:
        answer = run_external(
            args.provider,
            args.adapter_config.resolve(),
            prompt,
            cwd,
            args.allow_workspace_read,
            args.timeout_seconds,
            args.model,
            args.effort,
            args.max_budget_usd,
        )
    else:
        raise RuntimeError(
            f"Unknown provider {args.provider}; pass --adapter-config for external providers"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(answer, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"run_peer.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
