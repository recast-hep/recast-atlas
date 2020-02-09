import click


@click.group(help="Helper Commands for CI systems")
def ci():
    pass


@ci.command()
def cvmfs_helper():
    click.echo(
        "docker run -d --name cvmfs --pid=host --user 0 --privileged --restart always -v /shared-mounts:/cvmfsmounts:rshared gitlab-registry.cern.ch/vcs/cvmfs-automounter:master"
    )
