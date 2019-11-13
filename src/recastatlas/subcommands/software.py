import click
import subprocess
import os
from ..config import config


@click.group(help = 'Build Container Images for RECAST')
def software():
    pass


@software.command()
@click.argument('name')
@click.argument('path', default='.')
@click.option('--backend', type=click.Choice(['docker', 'kubernetes']), default = config.default_build_backend)
@click.option('--addr', default=config.backends['kubernetes']['buildkit_addr'])
@click.option('--push/--no-push', default=False)
def build(path, name, backend, addr,push):
    image = 'gitlab-registry.cern.ch/recast-atlas/images/{}'.format(name)
    path = os.path.abspath(path)
    if backend == 'kubernetes':
        subprocess.check_call(
            [
                'buildctl',
                '--addr',
                addr,
                'build',
                '--frontend',
                'dockerfile.v0',
                '--local',
                'context={}'.format(path),
                '--local',
                'dockerfile={}'.format(path),
                '--output',
                'type=image,name={},push={}'.format(image,'true' if push else 'false'),
            ]
        )
    elif backend == 'docker':
        subprocess.check_call(['docker', 'build', '-t', image, path])
        if push:
            subprocess.check_call(['docker', 'push', image])
