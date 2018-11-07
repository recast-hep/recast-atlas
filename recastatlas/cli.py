import click
import logging

from .subcommands.run import run
from .subcommands.catalogue import catalogue
from .subcommands.auth import auth

LOGFORMAT = '%(asctime)s | %(name)20.20s | %(levelname)6s | %(message)s'

@click.group()
@click.option('-l','--loglevel', default = 'WARNING')
def recastatlas(loglevel):
    logging.basicConfig(level=getattr(logging, loglevel), format=LOGFORMAT)

recastatlas.add_command(run,'run')
recastatlas.add_command(catalogue,'catalogue')
recastatlas.add_command(auth,'auth')


# recastatlas.add_command(software.software,'software')

# @recastatlas.group()
# def testdata():
#     pass
#
# @recastatlas.group()
# def fragment():
#     pass
#
#
# @recastatlas.group()
# def template():
#     pass

if __name__ == '__main__':
    recastatlas()
