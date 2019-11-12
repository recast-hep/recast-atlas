import click
from ..config import config
from ..backends import check_backend


@click.group(help="The RECAST computational backends.")
def backends():
    pass


@backends.command()
@click.option("--check/--no-check", default=False)
def ls(check):
    fmt = "{0:20}{1:60}{2:10}"
    click.secho(fmt.format("NAME", "DESCRIPTION", "STATUS"))
    for k, v in config.backends.items():
        if check:
            status = "OK" if check_backend(k) else "NOT OK"
        else:
            status = ""
        default = {"short_description": "no description given"}
        click.secho(
            fmt.format(k, v.get("metadata", default)["short_description"], status)
        )
