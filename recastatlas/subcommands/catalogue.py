import click
import yaml
from ..config import config

@click.group()
def catalogue():
    pass

@catalogue.command()
def ls():
    fmt = '{0:35}{1:60}{2:20}'
    click.secho(fmt.format('NAME','DESCRIPTION','EXAMPLES'))
    for k,v in config.catalogue.items():
        click.secho(fmt.format(k,v['metadata']['short_description'],','.join(list(v['example_inputs'].keys()))))

@catalogue.command()
@click.argument('name')
def describe(name):
    data = config.catalogue[name]
    toprint = '''\

{name:20}
--------------------
description  : {short:20}
author       : {author}
'''.format(
    author = data['metadata']['author'],
    name = name,
    short = data['metadata']['short_description']
    )
    click.secho(toprint)

@catalogue.command()
@click.argument('name')
@click.argument('example')
def example(name,example):
    data = config.catalogue[name]
    click.secho(yaml.dump(data['example_inputs'][example], default_flow_style = False))