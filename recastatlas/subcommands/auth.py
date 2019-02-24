import click
import sys
import os

envvar = [
'RECAST_AUTH_USERNAME',
'RECAST_AUTH_PASSWORD',
'YADAGE_SCHEMA_LOAD_TOKEN',
]

AUTH_LOC_VAR = 'PACKTIVITY_AUTH_LOCATION'


@click.group()
def auth():
    pass


@auth.command()
def setup():
    expt = 'ATLAS'
    if sys.stdout.isatty():
        click.secho('Sorry, we will not print your password to stdout. Use `eval $(recast auth setup)` to store your credentials in env variables', fg = 'red')
        raise click.Abort()

    username = click.prompt('Enter your username to authenticate as {}'.format(expt), hide_input = False, err = True)
    password = click.prompt('Enter your password for {} (VO: {})'.format(username,expt), hide_input = True, err = True)
    token    = click.prompt('Your GitLab token (optional, to access private workflows)'.format(username,expt), hide_input = True, err = True, default = '<none>')


    click.secho("export {}='{}'".format(envvar[0],username))
    click.secho("export {}='{}'".format(envvar[1],password))
    click.secho("export {}='{}'".format(envvar[2],token))
    click.secho('You password is stored in the environment variable {}. Run `eval $(recast auth destroy)` to clear your password or exit the shell.'.format(' and '.join(envvar)), err = True)

@auth.command()
@click.option('--basedir', default = None)
def write(basedir):
    basedir = basedir or os.getcwd()
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    krbfile = os.path.join(basedir,'getkrb.sh')
    with open(krbfile,'w') as f:
        f.write("echo '{}'|kinit {}@CERN.CH".format(
            os.environ[envvar[1]],os.environ[envvar[0]]
            )
        )
    os.chmod(krbfile, 0o755)
    click.secho('export {}={}'.format(AUTH_LOC_VAR,os.path.abspath(basedir)))



@auth.command()
def destroy():
    if sys.stdout.isatty():
        click.secho('Use eval $(recast auth destroy) to unset the variables', fg = 'red')
        raise click.Abort()
    click.secho('unset {}'.format(envvar[0]))
    click.secho('unset {}'.format(envvar[1]))
    click.secho('unset {}'.format(envvar[2]))

@auth.command()
@click.argument('location')
def use(location):
    click.secho('export {}={}'.format(AUTH_LOC_VAR,os.path.abspath(location)))
