import os
import click
import tempfile
import logging
import yaml
import uuid
import json

from ..config import config
from ..backends import run_sync, run_async
from ..resultsextraction import extract_results
log = logging.getLogger(__name__)    

def make_spec(name,data,inputs):
    spec = {
        'dataarg': name,
        'dataopts': inputs.get('dataopts',{}),
        'initdata': inputs['initdata'],
        'workflow': data['spec']['workflow'],
        'toplevel': data['spec']['toplevel'],
        'visualize': True
    }
    return spec

@click.command()
@click.argument('name')
@click.argument('inputdata', default = '')
@click.option('--example', default = 'default')
def run(name,inputdata,example):
    data      = config.catalogue[name]
    if inputdata:
        inputs = yaml.load(open(inputdata))
    else:
        try:
            inputs  = data['example_inputs'][example]
        except:
            raise click.ClickException("Example '{}' not found. Choose from {}".format(example, list(data['example_inputs'].keys())))


    name = "recast-{}".format(str(uuid.uuid1()).split('-')[0])
    spec = make_spec(name,data,inputs)


    backend = 'local'
    run_sync(name, spec, backend = backend)

    log.info('RECAST run finished.')

    result = extract_results(data['results'], spec['dataarg'], backend = backend)
    formatted_result = yaml.safe_dump(result, default_flow_style=False)
    click.secho('RECAST result:\n--------------\n{}'.format(formatted_result))

@click.command()
@click.argument('name')
@click.argument('inputdata', default = '')
@click.option('--example', default = 'default')
def submit(name,inputdata,example):
    data      = config.catalogue[name]
    if inputdata:
        inputs = yaml.load(open(inputdata))
    else:
        try:
            inputs  = data['example_inputs'][example]
        except:
            raise click.ClickException("Example '{}' not found. Choose from {}".format(example, list(data['example_inputs'].keys())))

    name = "recast-{}".format(str(uuid.uuid1()).split('-')[0])
    spec = make_spec(name,data,inputs)

    backend = 'kubernetes'
    rc = run_async(name, spec, backend = backend)
    click.secho("{} submitted".format(str(name)))

@click.command()
@click.argument('name')
@click.argument('instance')
@click.option('--show-url/--no-url', default = False)
@click.option('--tunnel/--no-tunnel', default = False)
def retrieve(name,instance, show_url, tunnel):
    backend = 'kubernetes'
    if show_url:
        from kubernetes import client as k8client
        from kubernetes import config as k8config
        k8config.load_kube_config()
        port = 30000

        tunnel_host = 'lxplus.cern.ch'

        host = '{}'.format(
            k8client.CoreV1Api().list_node().to_dict()['items'][0]['metadata']['name']
        )

        if tunnel:
            ssh_cmd = 'ssh -fNL {}:{}:{} {}'.format(port,host,port, tunnel_host)
            click.secho(ssh_cmd)
            host = '127.0.0.1'
        else:
            host = host + 'cern.ch'
        click.secho('http://{host}:{port}/{name}'.format(
            host = host,
            port = port,
            name = instance
        ))
        return
    data      = config.catalogue[name]
    result = extract_results(data['results'], instance, backend = backend)
    formatted_result = yaml.safe_dump(result, default_flow_style=False)
    click.secho('RECAST result:\n--------------\n{}'.format(formatted_result))

