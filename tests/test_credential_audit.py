from assessment.credential_audit import (
    build_hydra_command,
    build_john_command,
    run_hydra_authorized,
)


def test_hydra_builder_is_bounded_and_explicit(tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("one\ntwo\n", encoding="utf-8")
    command = build_hydra_command(
        target="127.0.0.1",
        username="labuser",
        wordlist=wordlist,
        protocol="http-post-form",
        port=8080,
        module_args="/training-login:username=^USER^&password=^PASS^:F=invalid credentials",
        threads=2,
    )
    assert command[0] == "hydra"
    assert command[command.index("-t") + 1] == "2"
    assert "-f" in command
    assert "127.0.0.1" in command


def test_hydra_builder_rejects_unbounded_threads(tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("one\n", encoding="utf-8")
    import pytest
    with pytest.raises(ValueError):
        build_hydra_command(
            target="127.0.0.1", username="labuser",
            wordlist=wordlist, protocol="ssh", threads=99,
        )


def test_hydra_authorization_blocks_before_execution(monkeypatch, tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("one\n", encoding="utf-8")
    called = []
    monkeypatch.setattr(
        "assessment.credential_audit.validate_scope",
        lambda **kwargs: (False, "not authorized"),
    )
    monkeypatch.setattr(
        "assessment.credential_audit.subprocess.run",
        lambda *args, **kwargs: called.append(args),
    )
    import pytest
    with pytest.raises(PermissionError):
        run_hydra_authorized(
            ssid="UNAUTHORIZED", bssid="00:11:22:33:44:55",
            authorization_ref="BAD", target="127.0.0.1",
            username="labuser", wordlist=wordlist,
            protocol="ssh", execute=True,
        )
    assert called == []


def test_hydra_defaults_to_dry_run(monkeypatch, tmp_path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("one\n", encoding="utf-8")
    monkeypatch.setattr(
        "assessment.credential_audit.validate_scope",
        lambda **kwargs: (True, "Authorized"),
    )
    result = run_hydra_authorized(
        ssid="LAB-NET", bssid="02:00:00:00:00:01",
        authorization_ref="LAB-001", target="127.0.0.1",
        username="labuser", wordlist=wordlist,
        protocol="ssh",
    )
    assert result.authorized is True
    assert result.executed is False
    assert result.returncode is None
    assert result.stdout.startswith("hydra ")


def test_john_builder(tmp_path):
    hashes = tmp_path / "hashes.txt"
    words = tmp_path / "words.txt"
    hashes.write_text("dummy", encoding="utf-8")
    words.write_text("one\n", encoding="utf-8")
    command = build_john_command(
        hash_file=hashes, wordlist=words, rules="Single",
    )
    assert command[0] == "john"
    assert f"--wordlist={words}" in command
    assert "--rules=Single" in command
