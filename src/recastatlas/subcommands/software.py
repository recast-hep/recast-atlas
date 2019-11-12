import click
import subprocess
import os

@click.group()
def software():
    pass


@software.command()
@click.argument('name', help = 'docker image name e.g. <group>/<name>')
@click.argument('path', default = '.', help = 'path to build context')
@click.option('--backend',type = click.Choice(['docker','kubernetes']))
@click.option('--addr',default = 'kube-pod://buildkitd')
def build(path,name,backend,addr):
    image = 'gitlab-registry.cern.ch/recast-atlas/images/{}'.format(name)
    path = os.path.abspath(path)
    if backend=='kubernetes':
        subprocess.check_call([
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
            'type=image,name={},push=true'.format(image)
            ]
        )
    elif backend=='docker':
        subprocess.check_call([
            'docker',
            'build',
            '-t',
            image,
            path
        ])
        subprocess.check_call([
            'docker',
            'push',
            image
        ]) 