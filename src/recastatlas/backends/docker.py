from ..config import config
from ..exceptions import FailedRunException
import logging
import os
import base64
import json
import textwrap
import subprocess
import yaml

log = logging.getLogger(__name__)

def setup_docker():
    backend = "docker"
    cwd = os.getcwd()
    image = config.backends[backend]["image"]

    special_envs = [
        'PACKTIVITY_CVMFS_LOCATION',
        'PACKTIVITY_CVMFS_PROPAGATION',
        'PACKTIVITY_AUTH_LOCATION',
        'YADAGE_SCHEMA_LOAD_TOKEN',
        'YADAGE_INIT_TOKEN',
    ]
    assert special_envs

    command = [
        "docker",
        "run",
        "--rm",
        "-i",
        "-v",
        "{}:{}".format(cwd, cwd),
        "-w",
        cwd,
        "-v",
        "/var/run/docker.sock:/var/run/docker.sock",
    ]

    if "cvmfs" in config.backends[backend]:
        command += [
            "-e",
            "PACKTIVITY_CVMFS_LOCATION={}".format(
                config.backends[backend]["cvmfs"]["location"]
            ),
        ]
        command += [
            "-e",
            "PACKTIVITY_CVMFS_PROPAGATION={}".format(
                config.backends[backend]["cvmfs"]["propagation"]
            ),
        ]

    if "auth_location" in config.backends[backend]:
        command += [
            "-e",
            "PACKTIVITY_AUTH_LOCATION={}".format(
                config.backends[backend]["auth_location"]
            ),
        ]
    if "schema_load_token" in config.backends[backend]:
        command += [
            "-e",
            "YADAGE_SCHEMA_LOAD_TOKEN={}".format(
                config.backends[backend]["schema_load_token"]
            ),
        ]
    if "private_token" in config.backends[backend]:
        command += [
            "-e",
            "YADAGE_INIT_TOKEN={}".format(config.backends[backend]["private_token"]),
        ]

    command += [image]

    dockerconfig = {}
    if config.backends[backend]["reg"]["host"]:
        dockerconfig = {
            "auths": {
                "gitlab-registry.cern.ch": {
                    "auth": base64.b64encode(
                        "{}:{}".format(
                            config.backends[backend]["reg"]["user"],
                            config.backends[backend]["reg"]["pass"],
                        ).encode("ascii")
                    ).decode("ascii")
                }
            }
        }
    return command, dockerconfig
    
class DockerBackend:
    def run_workflow(self,name,spec):
        backend_config = config.backends['docker']["fromstring"]

        spec["backend"] = spec.get('backend',backend_config)
        command, dockerconfig = setup_docker()

        script = """\
        mkdir -p ~/.docker
        echo '{dockerconfig}' > ~/.docker/config.json 
        cat << 'EOF' | yadage-run -f - 
        {spec}
        EOF
        """.format(
            spec=json.dumps(spec), dockerconfig=json.dumps(dockerconfig)
        )
        command += ["sh", "-c", textwrap.dedent(script)]
        subprocess.check_call(command)
        
    def run_packtivity(self,name,spec):
        workname = name
        command, dockerconfig = setup_docker()
        script = """\
mkdir -p ~/.docker
cat << 'EOF' > /tmp/pars.yml
{pars}
EOF
echo '{dockerconfig}' > ~/.docker/config.json 
packtivity-run {spec} -t {toplevel} /tmp/pars.yml -w {workname} {readdirs}
        """.format(
            spec=spec["spec"],
            dockerconfig=json.dumps(dockerconfig),
            workname=workname,
            toplevel=spec["toplevel"],
            pars=yaml.safe_dump(spec["parameters"], default_flow_style=False),
            readdirs=" ".join(
                ["-r {}".format(os.path.realpath(d)) for d in spec.get("data", [])]
            ),
        )
        command += ["sh", "-c", textwrap.dedent(script)]
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            raise FailedRunException

    def check_backend(self):
        try:
            rc = subprocess.check_call(
                ["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return rc == 0
        except:
            pass
        return False
