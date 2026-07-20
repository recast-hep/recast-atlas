from __future__ import annotations

import os
import shutil

import pytest
import yaml
from click.testing import CliRunner

from recastatlas.config import config
from recastatlas.engines.snakemake import (
    build_command,
    build_docker_command,
    parse_remote_toplevel,
    prepare_run,
)
from recastatlas.subcommands.catalogue import catalogue
from recastatlas.subcommands.run import make_spec, run, submit

has_snakemake = shutil.which("snakemake") is not None
has_docker = shutil.which("docker") is not None
docker_test_image = os.environ.get("RECAST_TEST_DOCKER_IMAGE")


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


def test_snakemake_submit_errors():
    runner = CliRunner()
    result = runner.invoke(submit, ["examples/snakehello", "--backend", "reana"])
    assert result.exit_code != 0
    assert "only support the local and docker backends" in result.output


def test_build_docker_command(monkeypatch):
    monkeypatch.delenv("RECAST_SNAKEMAKE_SDM", raising=False)
    monkeypatch.setenv("RECAST_DOCKER_IMAGE", "some/image:tag")
    cwd = os.getcwd()
    cmd = build_docker_command("Snakefile", "workdir", "config.yml")
    assert cmd[:8] == ["docker", "run", "--rm", "-i", "-v", f"{cwd}:{cwd}", "-w", cwd]
    assert "--privileged" not in cmd
    assert "some/image:tag" in cmd
    assert cmd.index("some/image:tag") < cmd.index("snakemake")

    monkeypatch.setenv("RECAST_SNAKEMAKE_SDM", "apptainer")
    cmd = build_docker_command("Snakefile", "workdir", "config.yml")
    assert "--privileged" in cmd
    assert cmd[-2:] == ["--software-deployment-method", "apptainer"]


def test_prepare_run_materialize(tmpdir):
    with tmpdir.as_cwd():
        spec = make_spec(
            "recast-mat", config.catalogue["examples/snakehello"], {"initdata": {}}
        )
        spec.pop("workflow_type")
        workdir, snakefile, configfile = prepare_run(spec, materialize=True)
        assert snakefile.startswith(os.path.join(workdir, "_recast_workflow"))
        assert os.path.isfile(snakefile)
        assert os.path.isfile(configfile)


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


@pytest.mark.skipif(
    not (has_docker and docker_test_image),
    reason="docker and RECAST_TEST_DOCKER_IMAGE required",
)
def test_run_snakehello_docker(tmpdir, monkeypatch):
    monkeypatch.setenv("RECAST_DOCKER_IMAGE", docker_test_image)
    with tmpdir.as_cwd():
        runner = CliRunner()
        result = runner.invoke(
            run,
            ["examples/snakehello", "--backend", "docker", "--tag", "dockersnake"],
        )
        assert result.exit_code == 0
        resultfile = "recast-dockersnake/results/result.yml"
        assert os.path.exists(resultfile)
        assert yaml.safe_load(open(resultfile)) == {"greeting": "Hello RECAST"}


@pytest.mark.skipif(not has_snakemake, reason="snakemake not installed")
def test_catalogue_check_snakemake():
    runner = CliRunner()
    result = runner.invoke(catalogue, ["check", "examples/snakehello"])
    assert result.exit_code == 0
    assert "Everything looks good" in result.output
