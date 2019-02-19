import os
import click
import tempfile
import logging
import yaml




from ..config import config
from ..backends import run_sync
from ..resultsextraction import extract_results
log = logging.getLogger(__name__)

@click.command()
@click.argument('name')
@click.argument('inputdata', default = '')
@click.option('--example', default = 'default')
def run(name,inputdata,example):
    data      = config.catalogue[name]
    if inputdata:
        inputdata = yaml.load(open(inputdata))['data']
    else:
        try:
            inputs  = data['example_inputs'][example]
        except:
            raise click.ClickException("Example '{}' not found. Choose from {}".format(example, list(data['example_inputs'].keys())))
        inputdata = inputs['data']

    log.info('executing RECAST configuration %s on input %s',name, inputdata)


    backend = 'local'

    dataarg = tempfile.mkdtemp(prefix = 'recast-',dir = os.curdir)
    spec = {
        'dataarg': dataarg,
        'initdata': inputdata,
        'workflow': data['spec']['workflow'],
        'toplevel': data['spec']['toplevel'],
        'visualize': True,
        'backendopts': {'purepubopts': {'exec': {'logging_level': 'WARNING'}}}
    }
    run_sync(spec, backend = backend)

    log.info('RECAST run finished.')

    result = extract_results(data['results'], spec, backend = backend)
    formatted_result = yaml.safe_dump(result, default_flow_style=False)
    click.secho('RECAST result:\n--------------\n{}'.format(formatted_result))
