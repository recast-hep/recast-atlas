import click
import logging

from .subcommands.run import run, submit, retrieve, status
from .subcommands.catalogue import catalogue
from .subcommands.auth import auth
from .subcommands.backends import backends
from .subcommands.testing import testing
from .subcommands.ci import ci
from .subcommands.software import software

LOGFORMAT = "%(asctime)s | %(name)20.20s | %(levelname)6s | %(message)s"


@click.group()
@click.option("-l", "--loglevel", default="INFO")
def recastatlas(loglevel):
    logging.basicConfig(level=getattr(logging, loglevel), format=LOGFORMAT)


recastatlas.add_command(run, "run")
recastatlas.add_command(submit, "submit")
recastatlas.add_command(retrieve, "retrieve")
recastatlas.add_command(status, "status")
recastatlas.add_command(catalogue, "catalogue")
recastatlas.add_command(auth, "auth")
recastatlas.add_command(backends, "backends")
recastatlas.add_command(ci, "ci")
recastatlas.add_command(testing, "tests")
recastatlas.add_command(software, "software")

if __name__ == "__main__":
    recastatlas()
