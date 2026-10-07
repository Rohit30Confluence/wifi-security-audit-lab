#!/usr/bin/env python3
"""Authorized credential-audit engine.

This module provides a guarded Hydra/John integration for assessment sessions.
It never bypasses the repository authorization model and defaults to dry-run.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from assessment.session import validate_scope


SUPPORTED_ONLINE_ENGINES = {"hydra"}
SUPPORTED_OFFLINE_ENGINES = {"john"}
SUPPORTED_HYDRA_PROTOCOLS = {
    "ftp", "http-get", "http-post-form", "https-get",
    "https-post-form", "ssh", "telnet",
}


@dataclass(frozen=True)
class AuditResult:
    engine: str
    authorized: bool
    executed: bool
    returncode: int | None
    stdout: str
    stderr: str
    reason: str


def _require_authorization(ssid: str, bssid: str | None, authorization_ref: str) -> None:
    valid, reason = validate_scope(
        ssid=ssid, bssid=bssid, authorization_ref=authorization_ref,
    )
    if not valid:
        raise PermissionError(f"Authorization validation failed: {reason}")


def build_hydra_command(
    *,
    target: str,
    username: str,
    wordlist: Path,
    protocol: str,
    port: int | None = None,
    module_args: str | None = None,
    threads: int = 2,
    stop_on_first: bool = True,
) -> list[str]:
    if protocol not in SUPPORTED_HYDRA_PROTOCOLS:
        raise ValueError(f"Unsupported Hydra protocol: {protocol}")
    if not target.strip():
        raise ValueError("Target is required")
    if not username:
        raise ValueError("Username is required")
    if not wordlist.is_file():
        raise FileNotFoundError(wordlist)
    if not 1 <= threads <= 16:
        raise ValueError("threads must be between 1 and 16")

    command = ["hydra", "-l", username, "-P", str(wordlist)]
    if port is not None:
        if not 1 <= port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        command += ["-s", str(port)]
    command += ["-t", str(threads)]
    if stop_on_first:
        command.append("-f")
    command += [target, protocol]
    if module_args:
        command.append(module_args)
    return command


def run_hydra_authorized(
    *,
    ssid: str,
    bssid: str | None,
    authorization_ref: str,
    target: str,
    username: str,
    wordlist: Path,
    protocol: str,
    port: int | None = None,
    module_args: str | None = None,
    threads: int = 2,
    timeout: int = 300,
    execute: bool = False,
) -> AuditResult:
    _require_authorization(ssid, bssid, authorization_ref)

    command = build_hydra_command(
        target=target, username=username, wordlist=wordlist,
        protocol=protocol, port=port, module_args=module_args,
        threads=threads,
    )

    if not execute:
        return AuditResult(
            engine="hydra", authorized=True, executed=False,
            returncode=None, stdout=" ".join(command), stderr="",
            reason="DRY_RUN: authorization passed; command not executed",
        )

    if shutil.which("hydra") is None:
        raise RuntimeError("Hydra executable not found")

    try:
        completed = subprocess.run(
            command, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return AuditResult(
            engine="hydra", authorized=True, executed=True,
            returncode=None, stdout=exc.stdout or "", stderr=exc.stderr or "",
            reason="Hydra execution timed out",
        )

    return AuditResult(
        engine="hydra", authorized=True, executed=True,
        returncode=completed.returncode, stdout=completed.stdout,
        stderr=completed.stderr, reason="Hydra execution completed",
    )


def build_john_command(
    *,
    hash_file: Path,
    wordlist: Path | None = None,
    rules: str | None = None,
) -> list[str]:
    if not hash_file.is_file():
        raise FileNotFoundError(hash_file)
    command = ["john"]
    if wordlist is not None:
        if not wordlist.is_file():
            raise FileNotFoundError(wordlist)
        command += [f"--wordlist={wordlist}"]
    if rules:
        command.append(f"--rules={rules}")
    command.append(str(hash_file))
    return command


def run_john_authorized(
    *,
    ssid: str,
    bssid: str | None,
    authorization_ref: str,
    hash_file: Path,
    wordlist: Path | None = None,
    rules: str | None = None,
    timeout: int = 300,
    execute: bool = False,
) -> AuditResult:
    _require_authorization(ssid, bssid, authorization_ref)
    command = build_john_command(
        hash_file=hash_file, wordlist=wordlist, rules=rules,
    )

    if not execute:
        return AuditResult(
            engine="john", authorized=True, executed=False,
            returncode=None, stdout=" ".join(command), stderr="",
            reason="DRY_RUN: authorization passed; command not executed",
        )

    if shutil.which("john") is None:
        raise RuntimeError("John executable not found")

    try:
        completed = subprocess.run(
            command, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return AuditResult(
            engine="john", authorized=True, executed=True,
            returncode=None, stdout=exc.stdout or "", stderr=exc.stderr or "",
            reason="John execution timed out",
        )

    return AuditResult(
        engine="john", authorized=True, executed=True,
        returncode=completed.returncode, stdout=completed.stdout,
        stderr=completed.stderr, reason="John execution completed",
    )
