import os
import yaml
import pkg_resources

class Config(object):
    @property
    def backends(self):
        return {
            'local': {
                'metadata': {
                    'short_description': 'runs locally'
                },
                'fromstring': 'multiproc:auto'
            },
            'kubernetes': {
                'metadata': {
                    'short_description': 'runs on a Kubernetes cluster'
                }
            }
        }
    @property
    def catalogue(self):
        cfg = yaml.safe_load(open(pkg_resources.resource_filename('recastatlas','data/config.yml')))
        if 'RECAST_ATLAS_CATALOGUE' in os.environ:
            newcfg = yaml.safe_load(open(os.environ.get('RECAST_ATLAS_CATALOGUE')))
            cfg.update(**newcfg)
        return cfg

config = Config()
