import os
import yaml
import pkg_resources
import glob
import logging

log = logging.getLogger(__name__)

def conf_from_env(var,default = None    ):
    v = os.environ.get(var)
    if v is not None:
        try:
            return yaml.safe_load(v)
        except:
            log.error(f'could not get config from env var {var} (value: {v})')
            raise
    return default
    

class Config(object):
    @property
    def default_run_backend(self):
        return os.environ.get('RECAST_DEFAULT_RUN_BACKEND','docker')

    def default_build_backend(self):
        return os.environ.get('RECAST_DEFAULT_BUILD_BACKEND','docker')

    @property
    def backends(self):
        return {
            "local": {
                "metadata": {
                    "short_description": "runs locally with natively installed tools"
                },
                "fromstring": conf_from_env("RECAST_LOCAL_BACKENDSTRING","multiproc:auto")
            },
            "docker": {
                "metadata": {"short_description": "runs with containerized tools"},
                "fromstring": conf_from_env("RECAST_DOCKER_BACKENDSTRING","multiproc:auto"),
                "image": conf_from_env("RECAST_DOCKER_IMAGE", "recast/recastatlas:v0.1.6"),
                "cvmfs": {"location": "/cvmfs", "propagation": "rprivate"},
                "reg": {
                    "user": conf_from_env("RECAST_REGISTRY_USERNAME"),
                    "pass": conf_from_env("RECAST_REGISTRY_PASSWORD"),
                    "host": conf_from_env("RECAST_REGISTRY_HOST"),
                },
                "schema_load_token": conf_from_env("YADAGE_SCHEMA_LOAD_TOKEN"),
                "init_token": conf_from_env("YADAGE_SCHEMA_LOAD_TOKEN"),
                "auth_location": conf_from_env("PACKTIVITY_AUTH_LOCATION"),
            },
            "kubernetes": {
                "metadata": {"short_description": "runs on a Kubernetes cluster"},
                "buildkit_addr": conf_from_env("RECAST_KUBERNETES_BUILDKIT_ADDR",'kube-pod://buildkitd'),
            },
            "reana": {
                "metadata": {"short_description": "runs on a REANA deployment"},
                "access_token": conf_from_env('REANA_ACCESS_TOKEN',None),
                "cvmfs_repos": conf_from_env('RECAST_REANA_CVMFS_REPOS',['atlas.cern.ch','atlas-condb.cern.ch'])
            }
        }

    def catalogue_paths(self,include_default = True):
        paths = [pkg_resources.resource_filename("recastatlas", "data/catalogue")] if include_default else []
        configpath = os.environ.get("RECAST_ATLAS_CATALOGUE")

        if configpath:
            for p in configpath.split(":"):
                paths.append(p)
        return paths

    @property
    def catalogue(self):
        cfg = {}
        files = []
        files += [x for p in self.catalogue_paths() for x in glob.glob("{}/*.yml".format(p))]
        files = list(set(files))
        log.debug(files)
        for f in files:
            d = yaml.safe_load(open(f))
            if not validate_catalogue_entry(d):
                continue
            log.debug(f'loading catalogue file {f}')
            name = d.pop("name")
            if not "toplevel" in d["spec"]:
                d["spec"]["toplevel"] = os.path.realpath(
                    os.path.join(os.path.dirname(f), "specs")
                )
            cfg[name] = d
        return cfg


config = Config()

def validate_catalogue_entry(entry):
    for x in ['name','metadata','spec']:
        if not x in entry:
            return False
    return True
