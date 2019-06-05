import yadageschemas
import logging
import subprocess
from .backends import run_sync_packtivity, get_shell_packtivity

log = logging.getLogger(__name__)


def validate_entry(data):
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
    except:
        pass
    return False


def run_test(name, testspec, backend):
    log.info("running test {}".format(name))
    try:
        run_sync_packtivity(name, testspec, backend=backend)
        return True
    except subprocess.CalledProcessError:
        log.warning("test failed")
    return False


def get_shell(name, testspec, backend):
    log.info("running test {}".format(name))
    cmdline = get_shell_packtivity(name, testspec, backend=backend)
    return cmdline
