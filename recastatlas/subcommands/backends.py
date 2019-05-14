import click
import yaml
from ..config import config
from ..backends import check_backend

@click.group()
def backends():
    pass

@backends.command()
@click.option('--check/--no-check', default = False)
def ls(check):
    fmt = '{0:20}{1:60}{2:10}'
    click.secho(fmt.format('NAME','DESCRIPTION','STATUS'))
    for k,v in config.backends.items():
        if check:
                status = 'OK' if check_backend(k) else 'NOT OK'
        else:
                status = ''
        click.secho(fmt.format(k,v['metadata']['short_description'],status))
        
