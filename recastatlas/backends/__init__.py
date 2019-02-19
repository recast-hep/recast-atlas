import click
import logging

log = logging.getLogger(__name__)

from ..config import config


def run_sync(spec, backend):
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
