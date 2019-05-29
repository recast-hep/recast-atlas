import click
import yaml
import os
import shutil
import string
import pkg_resources

from ..config import config
from ..testing import validate_entry

@click.group(help = 'The RECAST Analysis Catalogue')
def catalogue():
    pass

@catalogue.command()
@click.argument('name')
def check(name):
    data = config.catalogue[name]
    assert data
    valid = validate_entry(data)
    if not valid:
        click.secho('Sadly something is wrong :(')
    else:
        click.secho('Nice job! Everything looks good.', fg = 'green')

@catalogue.command()
@click.argument('name')
@click.argument('path')
def create(name,path):
    template_path = pkg_resources.resource_filename('recastatlas','data/templates/helloworld')
    shutil.copytree(template_path, path)
    recast_file = os.path.join(path,'recast.yml')
    data = string.Template(open(recast_file).read()).safe_substitute(name = name)
    with open(recast_file,'w') as f:
        f.write(data)
    click.secho('New skeleton created at {path}\nRun $(recast catalogue add {path}) to add to the catlogue'.format(path = path))


@catalogue.command()
@click.argument('path')
def add(path):
    if os.path.exists(path) and os.path.isdir(path):
        paths = []
        existing = os.environ.get('RECAST_ATLAS_CATALOGUE')
        if existing:
            paths.append(existing)
        paths.append(path)
        click.secho('export RECAST_ATLAS_CATALOGUE=' + ':'.join(paths))
    else:
        raise click.Abort('path {} does not exist or is not a directory'.format(path))

@catalogue.command()
def ls():
    fmt = '{0:35}{1:60}{2:20}'
    click.secho(fmt.format('NAME','DESCRIPTION','EXAMPLES'))
    
    default = {'short_description': 'no description given'}
    for k,v in sorted(config.catalogue.items(), key = lambda x: x[0]):
        click.secho(fmt.format(k,v.get('metadata',default)['short_description'],','.join(list(v.get('example_inputs',{}).keys()))))

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
    if not example in data.get('example_inputs',{}):
        click.secho('example not found.')
        return
    click.secho(yaml.dump(data['example_inputs'][example], default_flow_style = False))