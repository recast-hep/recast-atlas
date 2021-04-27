from reana_client.api.client import (
    create_workflow_from_json,
    get_workflow_status,
    ping,
    start_workflow,
    upload_to_server,
)
import os
import yadageschemas
import json
import contextlib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        self.auth_token = os.getenv("REANA_ACCESS_TOKEN")


    def submit(self, name, spec):
        print(name)
        

        wflowname = spec['dataarg']
        my_inputs = {
            "parameters": spec['initdata'],
        }
        
        _wflowfile = '_reana_wflow.json'

        ping(self.auth_token)
        result = create_workflow_from_json(
            workflow_engine="yadage",
            workflow_file=_wflowfile,
            name=wflowname,
            access_token=self.auth_token,
            parameters=my_inputs,
        )

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
            json.dump(wflowspec,wflowfile)

        abs_path_to_directories = [os.path.abspath(_wflowfile)]
        upload_to_server(wflowname, abs_path_to_directories, self.auth_token)
        os.remove(_wflowfile)



        operational_options = {}

        if 'dataopts' in spec and 'initdir' in spec['dataopts']:
            abs_initdir = os.path.abspath(spec['dataopts']['initdir'])
            base_initdir = os.path.basename(spec['dataopts']['initdir'])
            with working_directory(os.path.dirname(abs_initdir)):
                upload_to_server(wflowname, [abs_initdir], self.auth_token)
            operational_options['initdir'] = base_initdir

        start_workflow(wflowname, self.auth_token, {'operational_options': operational_options})

        return result

    def check_workflow(self, submission):
        status_details = get_workflow_status(submission['submission']['workflow_id'], self.auth_token)
        return status_details
