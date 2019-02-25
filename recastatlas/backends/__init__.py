import click
import logging

log = logging.getLogger(__name__)

from ..config import config


def run_sync(name, spec, backend):
    assert backend == 'local'

    backend_config = config.backends[backend]['fromstring']
    from yadage.utils import setupbackend_fromstring
    from yadage.steering_api import run_workflow
    spec['backend']  = setupbackend_fromstring(backend_config,spec.pop('backendopts',{}))

    try:
        run_workflow(**spec)
    except:
        log.exception('caught exception')
        exc = click.exceptions.ClickException(
            click.style("Workflow failed", fg='red')
        )
        exc.exit_code = 1
        raise exc
    
def run_async(name, spec, backend):
    assert backend == 'kubernetes'
    workflow = {
        'apiVersion': 'yadage.github.io/v1',
        'kind': 'Workflow',
        'metadata': {'name': name},
        'spec': spec
    }
    from kubernetes import client as k8sclient
    from kubernetes import config as k8sconfig
    k8sconfig.load_kube_config()
    _,rc,_ = k8sclient.ApiClient().call_api('/apis/yadage.github.io/v1/namespaces/default/workflows','POST', body = workflow) 
    return rc

