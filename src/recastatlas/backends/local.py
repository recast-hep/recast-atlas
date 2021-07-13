from yadage.utils import setupbackend_fromstring
from yadage.steering_api import run_workflow
from ..config import config
from ..exceptions import FailedRunException
import logging
import subprocess
import os

log = logging.getLogger(__name__)

class LocalBackend:
    def run_workflow(self, name, spec):
        backend_config = config.backends['local']["fromstring"]

        spec["backend"] = setupbackend_fromstring(
            backend_config, spec.pop("backendopts", {})
        )

        try:
            run_workflow(**spec)
        except:
            raise FailedRunException

    def run_packtivity(self, name, spec):
        workname = name
        import packtivity
        from packtivity.statecontexts import LocalFSState

        packspec = packtivity.load_packtivity(spec["spec"], toplevel=spec["toplevel"])
        p = packtivity.pack_object(packspec)
        s = LocalFSState(
            readwrite=[workname],
            readonly=[os.path.realpath(d) for d in spec.get("data", [])],
        )
        s.ensure()
        p(parameters=spec["parameters"], state=s)

    def check_backend(self):
        try:
            import yadage

            assert yadage
            rc = subprocess.check_call(
                ["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return rc == 0
        except:
            pass
        return False
