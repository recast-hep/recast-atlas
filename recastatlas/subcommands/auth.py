import click
import sys
import os
import shutil

envvar = {
    "auth_user": "RECAST_AUTH_USERNAME",
    "auth_pass": "RECAST_AUTH_PASSWORD",
    "spec_load": "YADAGE_SCHEMA_LOAD_TOKEN",
    "init_load": "YADAGE_INIT_TOKEN",
    "registry_user": "RECAST_REGISTRY_USERNAME",
    "registry_pass": "RECAST_REGISTRY_PASSWORD",
    "registry_host": "RECAST_REGISTRY_HOST",
    "auth_location": "PACKTIVITY_AUTH_LOCATION",
}


@click.group(help="Authentication Commands (to gain access to internal data)")
def auth():
    pass


@auth.command()
@click.option("-a", "--answer", multiple=True)
def setup(answer):
    expt = "ATLAS"
    if sys.stdout.isatty():
        click.secho(
            "Sorry, we will not print your password to stdout. Use `eval $(recast auth setup)` to store your credentials in env variables",
            fg="red",
        )
        raise click.Abort()

    questions = [
        (
            "username",
            {
                "str": "Enter your username to authenticate as {}".format(expt),
                "default": "none",
            },
        ),
        (
            "password",
            {
                "str": "Enter your password (VO: {})".format(expt),
                "hide": True,
                "default": "none",
            },
        ),
        (
            "token",
            {
                "str": "Your GitLab token (optional, to access private workflows and images)",
                "hide": True,
                "default": "none",
            },
        ),
        (
            "registry",
            {
                "str": "Your Docker image Registry (optional)",
                "default": "gitlab-registry.cern.ch",
            },
        ),
    ]

    answers = {}
    for i, (k, q) in enumerate(questions):
        if len(answer) > i:
            a = answer[i]
            if a == "default":
                a = q["default"]
        else:
            a = click.prompt(
                q["str"],
                hide_input=q.get("hide", False),
                err=q.get("err", True),
                default=q.get("default", "none"),
            )
        answers[k] = a
    username = answers["username"]
    password = answers["password"]
    token = answers["token"]
    registry = answers["registry"]

    click.secho("export {}='{}'".format(envvar["auth_user"], username))
    click.secho("export {}='{}'".format(envvar["auth_pass"], password))
    click.secho("export {}='{}'".format(envvar["spec_load"], token))
    click.secho("export {}='{}'".format(envvar["init_load"], token))
    click.secho("export {}='{}'".format(envvar["registry_host"], registry))
    click.secho("export {}='{}'".format(envvar["registry_user"], username))
    click.secho("export {}='{}'".format(envvar["registry_pass"], token))
    click.secho("docker login -u ${} -p ${} ${}".format(
        envvar["registry_user"],
        envvar["registry_pass"],
        envvar["registry_host"],
    ))
    click.secho(
        "You password is stored in the environment variables {}. Run `eval $(recast auth destroy)` to clear your password or exit the shell.".format(
            ",".join(envvar.values())
        ),
        err=True,
    )


@auth.command()
@click.option("--basedir", default=None)
def write(basedir):
    basedir = basedir or os.getcwd()
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    krbfile = os.path.join(basedir, "getkrb.sh")
    with open(krbfile, "w") as f:
        f.write(
            "echo '{}'|kinit {}@CERN.CH".format(
                os.environ[envvar["auth_pass"]], os.environ[envvar["auth_user"]]
            )
        )
    os.chmod(krbfile, 0o755)
    click.secho(
        "export {}={}".format(envvar["auth_location"], os.path.abspath(basedir))
    )


@auth.command()
def destroy():
    if sys.stdout.isatty():
        click.secho("Use eval $(recast auth destroy) to unset the variables", fg="red")
        raise click.Abort()
    for v in envvar.values():
        click.secho("unset {}".format(v))
    auth_loc = os.environ.get(envvar["auth_location"])
    if os.path.exists(auth_loc) and os.path.isdir(auth_loc):
        if os.path.exists(os.path.join(auth_loc, "getkrb.sh")):
            shutil.rmtree(auth_loc)


@auth.command()
@click.argument("location")
def use(location):
    click.secho(
        "export {}={}".format(envvar["auth_location"], os.path.abspath(location))
    )
