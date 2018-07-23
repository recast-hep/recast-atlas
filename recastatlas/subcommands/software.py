import click

@click.group()
@click.argument('spec')
def software():
    pass

@software.command()
def add():
    pass
