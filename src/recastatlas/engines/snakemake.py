from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import tempfile

import yaml

from ..config import config
from ..exceptions import BackendNotAvailableException, FailedRunException

log = logging.getLogger(__name__)

CONFIGFILE_NAME = "_recast_snakemake_config.yml"
CHECKOUT_DIRNAME = "_recast_workflow"
_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def parse_remote_toplevel(toplevel):
    """Parse 'github:org/repo[@ref][:subpath]' into (clone_url, ref, subpath)."""
    fields = toplevel.split(":")[1:]
    repospec, subpath = (fields[0], fields[1]) if len(fields) > 1 else (fields[0], "")
    repo, _, ref = repospec.partition("@")
    return f"https://github.com/{repo}.git", ref or None, subpath


def resolve_toplevel(toplevel, workdir, materialize=False):
    """Return the directory containing the workflow sources.

    Local toplevels are used in place; 'github:' toplevels are cloned into
    the instance workdir so the run stays self-contained. With materialize,
    local toplevels are also copied into the workdir so that the sources
    are visible when only the workdir is mounted into a container.
    """
    if toplevel.startswith("github:"):
        url, ref, subpath = parse_remote_toplevel(toplevel)
        checkout = os.path.join(workdir, CHECKOUT_DIRNAME)
        if not os.path.exists(checkout):
            if ref and _SHA_RE.match(ref):
                subprocess.run(["git", "clone", "--quiet", url, checkout], check=True)
                subprocess.run(
                    ["git", "-C", checkout, "checkout", "--quiet", ref], check=True
                )
            else:
                cmd = ["git", "clone", "--quiet", "--depth", "1"]
                if ref:
                    cmd += ["--branch", ref]
                subprocess.run([*cmd, url, checkout], check=True)
        return os.path.join(checkout, subpath) if subpath else checkout
    if toplevel.startswith("gitlab-cern:"):
        msg = "gitlab-cern toplevels are not yet supported for snakemake workflows"
        raise FailedRunException(msg)
    srcdir = os.path.realpath(toplevel)
    if materialize:
        checkout = os.path.join(workdir, CHECKOUT_DIRNAME)
        if not os.path.exists(checkout):
            shutil.copytree(srcdir, checkout)
        return checkout
    return srcdir


def _sdm_list():
    sdm = config.backends["local"]["snakemake"]["sdm"]
    if not sdm or sdm == "none":
        return []
    return [sdm] if isinstance(sdm, str) else list(sdm)


def build_snakemake_argv(snakefile, workdir, configfile, exe):
    snake_cfg = config.backends["local"]["snakemake"]
    argv = [
        exe,
        "--snakefile",
        snakefile,
        "--directory",
        workdir,
        "--configfile",
        configfile,
        "--cores",
        str(snake_cfg["cores"]),
    ]
    sdm = _sdm_list()
    if sdm:
        argv += ["--software-deployment-method", *sdm]
    return argv


def build_command(snakefile, workdir, configfile):
    exe = shutil.which("snakemake")
    if exe is None:
        msg = (
            "snakemake executable not found."
            " Install it with: python -m pip install 'recast-atlas[snakemake]'"
        )
        raise BackendNotAvailableException(msg)
    return build_snakemake_argv(snakefile, workdir, configfile, exe)


def build_docker_command(snakefile, workdir, configfile):
    cwd = os.getcwd()
    docker_cfg = config.backends["docker"]
    cmd = ["docker", "run", "--rm", "-i", "-v", f"{cwd}:{cwd}", "-w", cwd]
    if docker_cfg.get("platform"):
        cmd += ["--platform", docker_cfg["platform"]]
    # apptainer needs elevated privileges when run inside a docker container
    if any(s in ("apptainer", "singularity") for s in _sdm_list()):
        cmd += ["--privileged"]
    # persist pulled per-rule images in the instance workdir across runs
    cmd += ["-e", "APPTAINER_CACHEDIR={}".format(os.path.join(workdir, ".apptainer"))]
    cmd += [docker_cfg["image"]]
    cmd += build_snakemake_argv(snakefile, workdir, configfile, exe="snakemake")
    return cmd


def prepare_run(spec, materialize=False):
    """Set up the instance workdir and return (workdir, snakefile, configfile)."""
    workdir = os.path.realpath(spec["dataarg"])
    os.makedirs(workdir, exist_ok=True)

    initdir = spec.get("dataopts", {}).get("initdir")
    if initdir:
        shutil.copytree(os.path.realpath(initdir), workdir, dirs_exist_ok=True)

    srcdir = resolve_toplevel(spec["toplevel"], workdir, materialize=materialize)
    snakefile = os.path.join(srcdir, spec["workflow"])

    configfile = os.path.join(workdir, CONFIGFILE_NAME)
    with open(configfile, "w") as f:
        yaml.safe_dump(spec.get("initdata") or {}, f)

    return workdir, snakefile, configfile


def _run_or_raise(cmd):
    log.info("running snakemake: %s", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except (subprocess.CalledProcessError, OSError):
        log.exception("snakemake run failed")
        raise FailedRunException


def run_workflow_local(name, spec):
    workdir, snakefile, configfile = prepare_run(spec)
    _run_or_raise(build_command(snakefile, workdir, configfile))


def run_workflow_docker(name, spec):
    workdir, snakefile, configfile = prepare_run(spec, materialize=True)
    _run_or_raise(build_docker_command(snakefile, workdir, configfile))


def validate_workflow(data):
    """Validate a snakemake catalogue entry (used by `recast catalogue check`)."""
    with tempfile.TemporaryDirectory() as tmp:
        try:
            srcdir = resolve_toplevel(data["spec"]["toplevel"], tmp)
        except (subprocess.CalledProcessError, FailedRunException):
            return False
        snakefile = os.path.join(srcdir, data["spec"]["workflow"])
        if not os.path.isfile(snakefile):
            return False

        exe = shutil.which("snakemake")
        if exe is None:
            log.warning(
                "snakemake not installed; only verified that the Snakefile exists"
            )
            return True

        initdata = (data.get("example_inputs", {}).get("default") or {}).get(
            "initdata", {}
        )
        configfile = os.path.join(tmp, CONFIGFILE_NAME)
        with open(configfile, "w") as f:
            yaml.safe_dump(initdata or {}, f)
        proc = subprocess.run(
            [
                exe,
                "--snakefile",
                snakefile,
                "--directory",
                tmp,
                "--configfile",
                configfile,
                "--dry-run",
                "--quiet",
            ],
            capture_output=True,
            check=False,
        )
        return proc.returncode == 0
