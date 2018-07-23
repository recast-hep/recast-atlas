import click
from ..config import config

@click.group()
def catalogue():
    pass

@catalogue.command()
def ls():
    fmt = '{0:20}{1:20}'
    click.secho(fmt.format('NAME','DESCRIPTION'))
    for k,v in config.catalogue.items():
        click.secho(fmt.format(k,v['metadata']['short_description']))

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
