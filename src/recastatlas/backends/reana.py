from reana_client.api.client import (
    get_workflow_status,
    ping,
    start_workflow,
    upload_to_server,
)
from reana_commons.api_client import get_current_api_client
import os
import yadageschemas
import json
import contextlib
import urllib3
from ..config import config
from .. import exceptions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
log = logging.getLogger(__name__)

@contextlib.contextmanager
def working_directory(path):
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
        
class ReanaBackend:
    def __init__(self):
        self.auth_token = config.backends['reana']['access_token']
        self.cvmfs_repos = config.backends['reana']['cvmfs_repos']
        if not self.check_backend():
            raise exceptions.BackendNotAvailableException('no REANA auth found')

    def submit(self, name, spec):
        wflowname = spec['dataarg']
        my_inputs = {
            "parameters": spec['initdata'],
        }
        
        _wflowfile = '_reana_wflow.json'

        ping(self.auth_token)

        reana_yaml ={
            'inputs': {
                'parameters': my_inputs['parameters']
            },
            'workflow': {
                'type': 'yadage',
                'file': _wflowfile,
                'resources': {
                    'cvmfs': self.cvmfs_repos
                }
            }
        }

        client = get_current_api_client('reana-server')
        d = client.api.create_workflow(reana_specification = reana_yaml, workflow_name=wflowname, access_token = self.auth_token)
        result = d.response().result    
        
        with open(_wflowfile,'w') as wflowfile:
            wflowspec = yadageschemas.load(
                spec['workflow'],
                {
                    'toplevel': spec['toplevel'],
                    'load_as_ref': False,
                    'schema_name': 'yadage/workflow-schema',
                    'schemadir': yadageschemas.schemadir
                },
                {}
            )
            json.dump(wflowspec,wflowfile, indent = 4)

        abs_path_to_directories = [os.path.abspath(_wflowfile)]
        upload_to_server(wflowname, abs_path_to_directories, self.auth_token)
        os.remove(_wflowfile)



        operational_options = {}

        if 'dataopts' in spec and 'initdir' in spec['dataopts']:
            abs_initdir = os.path.abspath(spec['dataopts']['initdir'])
            base_initdir = os.path.basename(spec['dataopts']['initdir'])
            with working_directory(os.path.dirname(abs_initdir)):
                log.debug('uploading dir {abs_initdir}')
                upload_to_server(wflowname, [abs_initdir], self.auth_token)
            operational_options['initdir'] = base_initdir

        start_workflow(wflowname, self.auth_token, {'operational_options': operational_options})

        return result

    def check_workflow(self, submission):
        status_details = get_workflow_status(submission['submission']['workflow_id'], self.auth_token)
        return status_details

    def check_backend(self):
        try:
            assert self.auth_token
            result = ping(self.auth_token)
            return not(result['error'])
        except:
            return False