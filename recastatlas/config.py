import os
import yaml
import pkg_resources
import glob


class Config(object):
    @property
    def backends(self):
        return {
            "local": {
                "metadata": {
                    "short_description": "runs locally with natively installed tools"
                },
                "fromstring": "multiproc:auto",
            },
            "docker": {
                "metadata": {"short_description": "runs with containerized tools"},
                "image": "yadage/yadage:v0.19.9",
                "reg": {
                    "user": os.environ.get("RECAST_REGISTRY_USERNAME"),
                    "pass": os.environ.get("RECAST_REGISTRY_PASSWORD"),
                    "host": os.environ.get("RECAST_REGISTRY_HOST"),
                },
                "schema_load_token": os.environ.get("YADAGE_SCHEMA_LOAD_TOKEN"),
                "init_token": os.environ.get("YADAGE_SCHEMA_LOAD_TOKEN"),
                "auth_location": os.environ.get("PACKTIVITY_AUTH_LOCATION"),
            },
            "kubernetes": {
                "metadata": {"short_description": "runs on a Kubernetes cluster"}
            },
        }

    @property
    def catalogue(self):
        paths = [pkg_resources.resource_filename("recastatlas", "data/catalogue")]
        configpath = os.environ.get("RECAST_ATLAS_CATALOGUE")

        if configpath:
            for p in configpath.split(":"):
                paths.append(p)

        cfg = {}
        files = [x for p in paths for x in glob.glob("{}/*.yml".format(p))]
        for f in files:
            d = yaml.safe_load(open(f))
            if not validate_catalogue_entry(d):
                continue
            name = d.pop("name")
            if not "toplevel" in d["spec"]:
                d["spec"]["toplevel"] = os.path.realpath(
                    os.path.join(os.path.dirname(f), "specs")
                )
            cfg[name] = d
        return cfg


config = Config()


def validate_catalogue_entry(entry):
    return True
