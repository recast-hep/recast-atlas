import click
import sys
import os

envvar = {
 'auth_user': 'RECAST_AUTH_USERNAME',
 'auth_pass': 'RECAST_AUTH_PASSWORD',
 'spec_load': 'YADAGE_SCHEMA_LOAD_TOKEN',
 'registry_user': 'RECAST_REGISTRY_USERNAME',
 'registry_pass': 'RECAST_REGISTRY_PASSWORD',
}

AUTH_LOC_VAR = 'PACKTIVITY_AUTH_LOCATION'


@click.group(help = 'Authentication Commands (to gain access to internal data)')
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




    click.secho("export {}='{}'".format(envvar['auth_user'],username))
    click.secho("export {}='{}'".format(envvar['auth_pass'],password))
    click.secho("export {}='{}'".format(envvar['spec_load'],token))
    click.secho("export {}='{}'".format(envvar['registry_user'],username))
    click.secho("export {}='{}'".format(envvar['registry_pass'],token))
    click.secho('You password is stored in the environment variables {}. Run `eval $(recast auth destroy)` to clear your password or exit the shell.'.format(','.join(envvar.values())), err = True)

@auth.command()
@click.option('--basedir', default = None)
def write(basedir):
    basedir = basedir or os.getcwd()
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    krbfile = os.path.join(basedir,'getkrb.sh')
    with open(krbfile,'w') as f:
        f.write("echo '{}'|kinit {}@CERN.CH".format(
            os.environ[envvar['auth_user']],os.environ[envvar['auth_pass']]
            )
        )
    os.chmod(krbfile, 0o755)
    click.secho('export {}={}'.format(AUTH_LOC_VAR,os.path.abspath(basedir)))



@auth.command()
def destroy():
    if sys.stdout.isatty():
        click.secho('Use eval $(recast auth destroy) to unset the variables', fg = 'red')
        raise click.Abort()
    for v in envvar.values():
        click.secho('unset {}'.format(v))

@auth.command()
@click.argument('location')
def use(location):
    click.secho('export {}={}'.format(AUTH_LOC_VAR,os.path.abspath(location)))
