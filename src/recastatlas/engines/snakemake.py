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


def resolve_toplevel(toplevel, workdir):
    """Return the directory containing the workflow sources.

    Local toplevels are used in place; 'github:' toplevels are cloned into
    the instance workdir so the run stays self-contained.
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
    return os.path.realpath(toplevel)


def build_command(snakefile, workdir, configfile):
    exe = shutil.which("snakemake")
    if exe is None:
        msg = (
            "snakemake executable not found."
            " Install it with: python -m pip install 'recast-atlas[snakemake]'"
        )
        raise BackendNotAvailableException(msg)
    snake_cfg = config.backends["local"]["snakemake"]
    cmd = [
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
    sdm = snake_cfg["sdm"]
    if sdm and sdm != "none":
        cmd += [
            "--software-deployment-method",
            *([sdm] if isinstance(sdm, str) else list(sdm)),
        ]
    return cmd


def run_workflow_local(name, spec):
    workdir = os.path.realpath(spec["dataarg"])
    os.makedirs(workdir, exist_ok=True)

    initdir = spec.get("dataopts", {}).get("initdir")
    if initdir:
        shutil.copytree(os.path.realpath(initdir), workdir, dirs_exist_ok=True)

    srcdir = resolve_toplevel(spec["toplevel"], workdir)
    snakefile = os.path.join(srcdir, spec["workflow"])

    configfile = os.path.join(workdir, CONFIGFILE_NAME)
    with open(configfile, "w") as f:
        yaml.safe_dump(spec.get("initdata") or {}, f)

    cmd = build_command(snakefile, workdir, configfile)
    log.info("running snakemake: %s", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except (subprocess.CalledProcessError, OSError):
        log.exception("snakemake run failed")
        raise FailedRunException


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
