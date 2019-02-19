import click
import yaml
from ..config import config

@click.group()
def backends():
    pass

@backends.command()
def ls():
    fmt = '{0:20}{1:60}'
    click.secho(fmt.format('NAME','DESCRIPTION'))
    for k,v in config.backends.items():
        click.secho(fmt.format(k,v['metadata']['short_description']))
