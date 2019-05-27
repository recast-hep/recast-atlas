import os
import yaml
import pkg_resources
import glob

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
        paths = [pkg_resources.resource_filename('recastatlas','data/catalogue')]
        configpath = os.environ.get('RECAST_ATLAS_CATALOGUE')
        
        if configpath:
            for p in configpath.split(':'):
                paths.append(p)
        

        cfg = {}
        files = [x for p in paths for x in glob.glob('{}/*.yml'.format(p))]
        for f in files:
            d = yaml.safe_load(open(f))
            name = d.pop('name')
            cfg[name] =  d
        return cfg

config = Config()
