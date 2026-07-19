from __future__ import annotations

import os
import shutil

import pytest
import yaml
from click.testing import CliRunner

from recastatlas.config import config
from recastatlas.engines.snakemake import build_command, parse_remote_toplevel
from recastatlas.subcommands.catalogue import catalogue
from recastatlas.subcommands.run import make_spec, run

has_snakemake = shutil.which("snakemake") is not None


def test_catalogue_has_snakemake_entry():
    entry = config.catalogue["examples/snakehello"]
    assert entry["spec"]["workflow_type"] == "snakemake"
    assert "workflow_type" not in config.catalogue["testing/busyboxtest"]["spec"]


def test_make_spec_workflow_type():
    inputs = {"initdata": {}}
    yadage_spec = make_spec("recast-x", config.catalogue["testing/busyboxtest"], inputs)
    assert yadage_spec["workflow_type"] == "yadage"

    snake_spec = make_spec("recast-x", config.catalogue["examples/snakehello"], inputs)
    assert snake_spec["workflow_type"] == "snakemake"


def test_parse_remote_toplevel():
    assert parse_remote_toplevel("github:org/repo@main:sub/dir") == (
        "https://github.com/org/repo.git",
        "main",
        "sub/dir",
    )
    assert parse_remote_toplevel("github:org/repo") == (
        "https://github.com/org/repo.git",
        None,
        "",
    )
    assert parse_remote_toplevel("github:org/repo:sub") == (
        "https://github.com/org/repo.git",
        None,
        "sub",
    )


@pytest.mark.skipif(not has_snakemake, reason="snakemake not installed")
def test_build_command(monkeypatch):
    monkeypatch.delenv("RECAST_SNAKEMAKE_SDM", raising=False)
    cmd = build_command("Snakefile", "workdir", "config.yml")
    assert "--software-deployment-method" not in cmd
    assert cmd[1:] == [
        "--snakefile",
        "Snakefile",
        "--directory",
        "workdir",
        "--configfile",
        "config.yml",
        "--cores",
        "all",
    ]

    monkeypatch.setenv("RECAST_SNAKEMAKE_SDM", "conda")
    monkeypatch.setenv("RECAST_SNAKEMAKE_CORES", "4")
    cmd = build_command("Snakefile", "workdir", "config.yml")
    assert cmd[-2:] == ["--software-deployment-method", "conda"]
    assert "4" in cmd


def test_snakemake_wrong_backend_errors():
    runner = CliRunner()
    result = runner.invoke(run, ["examples/snakehello", "--backend", "docker"])
    assert result.exit_code != 0
    assert "only support --backend local" in result.output


@pytest.mark.skipif(not has_snakemake, reason="snakemake not installed")
def test_run_snakehello(tmpdir):
    with tmpdir.as_cwd():
        runner = CliRunner()
        result = runner.invoke(
            run,
            ["examples/snakehello", "--backend", "local", "--tag", "snakehello"],
        )
        assert result.exit_code == 0
        resultfile = "recast-snakehello/results/result.yml"
        assert os.path.exists(resultfile)
        assert yaml.safe_load(open(resultfile)) == {"greeting": "Hello RECAST"}
        assert "Hello RECAST" in result.output


@pytest.mark.skipif(not has_snakemake, reason="snakemake not installed")
def test_catalogue_check_snakemake():
    runner = CliRunner()
    result = runner.invoke(catalogue, ["check", "examples/snakehello"])
    assert result.exit_code == 0
    assert "Everything looks good" in result.output
