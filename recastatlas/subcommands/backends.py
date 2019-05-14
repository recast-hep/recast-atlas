import click
import yaml
from ..config import config
from ..backends import check_backend

@click.group()
def backends():
    pass

@backends.command()
def ls():
    fmt = '{0:20}{1:60}{2:10}'
    click.secho(fmt.format('NAME','DESCRIPTION','STATUS'))
    for k,v in config.backends.items():
        click.secho(fmt.format(k,v['metadata']['short_description'],'OK' if check_backend(k) else 'NOT OK'))
        
