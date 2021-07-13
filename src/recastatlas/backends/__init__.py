import json
import logging
import subprocess
import os
import textwrap
import shlex
from .. import exceptions

log = logging.getLogger(__name__)

BACKENDS = {}
try:
    from .reana import ReanaBackend
    BACKENDS['reana'] = ReanaBackend()
except (ImportError, exceptions.BackendNotAvailableException):
    pass

try:
    from .kubernetes import KubernetesBackend
    BACKENDS['kubernetes'] = KubernetesBackend()
except (ImportError, exceptions.BackendNotAvailableException):
    pass

try:
    from .local import LocalBackend
    BACKENDS['local'] = LocalBackend()
except (ImportError, exceptions.BackendNotAvailableException):
    pass

try:
    from .docker import DockerBackend
    from .docker import setup_docker
    BACKENDS['docker'] = DockerBackend()
except (ImportError, exceptions.BackendNotAvailableException):
    pass


def get_shell_packtivity(name, spec, backend):
    workname = name
    shellcmd = "packtivity-util shell {spec} -t {toplevel}  -w {workname} {readdirs}".format(
        spec=spec["spec"],
        toplevel=spec["toplevel"],
        workname=workname,
        readdirs=" ".join(
            ["-r {}".format(os.path.realpath(d)) for d in spec.get("data", [])]
        ),
    )
    if backend == "local":
        return subprocess.check_output(shlex.split(shellcmd)).decode("ascii")
    if backend == "docker":
        command, dockerconfig = setup_docker()
        script = """\
mkdir -p ~/.docker
echo '{dockerconfig}' > ~/.docker/config.json 
{command}
        """.format(
            dockerconfig=json.dumps(dockerconfig), command=shellcmd
        )
        command += ["sh", "-c", textwrap.dedent(script)]
        return subprocess.check_output(command).decode("ascii")


def run_sync_packtivity(name, spec, backend):
    assert backend in ["local", "docker"]
    BACKENDS[backend].run_packtivity(name, spec)

def run_sync(name, spec, backend):
    assert backend in ["local", "docker"]
    BACKENDS[backend].run_workflow(name,spec)

def run_async(name, spec, backend):
    assert backend in ["kubernetes", "reana"]
    return BACKENDS[backend].submit(name, spec)

def check_async(name, backend):
    assert backend in ["kubernetes", "reana"]
    return BACKENDS[backend].check_workflow(name)

def check_backend(backend):
    return BACKENDS[backend].check_backend()
    
def install_backend(backend):
    pass
