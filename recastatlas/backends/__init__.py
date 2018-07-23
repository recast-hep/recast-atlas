import click
import logging

log = logging.getLogger(__name__)
def run_sync(spec, backend):
    assert backend == 'local'

    from yadage.utils import setupbackend_fromstring
    from yadage.steering_api import run_workflow
    spec['backend']  = setupbackend_fromstring('multiproc:auto',spec.pop('backendopts',{}))

    try:
        run_workflow(**spec)
    except:
        log.exception('caught exception')
        exc = click.exceptions.ClickException(
            click.style("Workflow failed", fg='red')
        )
        exc.exit_code = 1
        raise exc
