from __future__ import annotations

import logging
import subprocess

import yadageschemas

from .backends import get_shell_packtivity, run_sync_packtivity

log = logging.getLogger(__name__)


def validate_entry(data):
    workflow_type = data["spec"].get("workflow_type", "yadage")
    if workflow_type == "snakemake":
        from .engines.snakemake import validate_workflow

        return validate_workflow(data)
    if workflow_type != "yadage":
        log.warning("unknown workflow_type %s", workflow_type)
        return False

    toplevel = data["spec"]["toplevel"]
    workflow = data["spec"]["workflow"]
    try:
        yadageschemas.load(
            workflow,
            specopts={
                "toplevel": toplevel,
                "load_as_ref": False,
                "schema_name": "yadage/workflow-schema",
                "schemadir": yadageschemas.schemadir,
            },
            validopts={
                "schemadir": yadageschemas.schemadir,
                "schema_name": "yadage/workflow-schema",
            },
        )
        return True
    except Exception:  # TODO: Specify Exception type
        pass
    return False


def run_test(name, testspec, backend):
    log.info(f"running test {name}")
    try:
        run_sync_packtivity(name, testspec, backend=backend)
        return True
    except subprocess.CalledProcessError:
        log.warning("test failed")
    return False


def get_shell(name, testspec, backend):
    log.info(f"running test {name}")
    cmdline = get_shell_packtivity(name, testspec, backend=backend)
    return cmdline
