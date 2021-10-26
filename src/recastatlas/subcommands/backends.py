import click
from ..config import config
from ..backends import check_backend
from recastatlas.exceptions import BackendNotAvailableException


@click.group(help="The RECAST computational backends.")
def backends():
    pass


@backends.command()
@click.option("--check/--no-check", default=False)
def ls(check):
    fmt = "{0:20}{1:60}{2:10}"
    click.secho(fmt.format("NAME", "DESCRIPTION", "STATUS"))
    for backend, conf in config.backends.items():
        if check:
            try:
                status = "OK" if check_backend(backend) else "NOT OK"
            except BackendNotAvailableException:
                # check_backend is performed by iterating through the global
                # dict recastatlas.backends.BACKENDS and checking each backend
                # key. If a backend is missing from the installation it will
                # not be loaded into the dict and will raise a
                # recastatlas.exceptions.BackendNotAvailableException.
                status = "NOT AVAILABLE"
        else:
            status = ""
        default = {"short_description": "no description given"}
        click.secho(
            fmt.format(
                backend, conf.get("metadata", default)["short_description"], status
            )
        )
