import click
import sys
import os
import re
import shutil
from ..backends import run_sync_packtivity
from ..config import config

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
    click.secho(
        "docker login -u ${} -p ${} ${}".format(
            envvar["registry_user"], envvar["registry_pass"], envvar["registry_host"]
        )
    )
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
@click.argument("image", default="gitlab-registry.cern.ch/lheinric/atlasonlytestimages")
@click.option("--backend", type=click.Choice(["local", "docker"]), default=config.default_run_backend)
def check_access_image(image,backend):

    if envvar["registry_user"] not in os.environ:
        raise RuntimeError("run `eval $(recast auth setup)` first")

    image = image.split(":", 1)
    if len(image) > 1:
        image, tag = image
    else:
        image = image[0]
        tag = "latest"

    spec = """
process:
    process_type: 'interpolated-script-cmd'
    script: 'echo hello world'
publisher:
    publisher_type: 'interpolated-pub'
    publish: {{}}
environment:
    environment_type: 'docker-encapsulated'
    image: {image}
    imagetag: {tag}
    """.format(
        image=image, tag=tag
    )

    testspec = "testimage.yml"
    open(testspec, "w").write(spec)

    testingdir = "recast-auth-testing-image"
    click.secho("Running test job for accessing image {}:{}".format(image, tag))
    click.secho(
        "Note: if the image {}:{} is not yet available locally, it will be pulled".format(
            image, tag
        )
    )
    click.secho("-" * 20)
    if os.path.exists(testingdir):
        shutil.rmtree(testingdir)

    run_sync_packtivity(
        testingdir,
        {"spec": testspec, "toplevel": os.getcwd(), "parameters": {}},
        backend=backend,
    )

    with open("{}/_packtivity/packtivity_syncbackend.run.log".format(testingdir)) as f:
        logfile = f.read()

    log_ok = "hello world" in logfile
    click.secho("-" * 20)
    click.secho("Access: {}".format("ok" if log_ok else "not ok"))


@auth.command()
@click.option("--image", default="lukasheinrich/xrootdclient:latest")
@click.argument(
    "location",
    default="root://eosuser.cern.ch//eos/project/r/recast/atlas/testauth/testfile.txt",
)
@click.option("--backend", type=click.Choice(["local", "docker"]), default=config.default_run_backend)
def check_access_xrootd(image, location,backend):

    image = image.split(":", 1)
    if len(image) > 1:
        image, tag = image
    else:
        image = image[0]
        tag = "latest"

    if "PACKTIVITY_AUTH_LOCATION" not in os.environ:
        click.echo(
            "Need to run `recast auth setup` and `recast auth write` or `recast auth use` first"
        )
        raise click.Abort()

    server = re.search("root://.*.cern.ch/", location).group(0)
    path = location.replace(server, "")

    spec = """
process:
    process_type: 'interpolated-script-cmd'
    script: |
        /recast_auth/getkrb.sh
        klist
        xrdfs {server} stat {path}
publisher:
    publisher_type: 'interpolated-pub'
    publish: {{}}
environment:
    environment_type: 'docker-encapsulated'
    image: {image}
    imagetag: {tag}
    resources:
    - GRIDProxy
    """.format(
        image=image, tag=tag, server=server, path=path
    )

    testspec = "testauth.yml"
    open(testspec, "w").write(spec)

    testingdir = "recast-auth-testing"
    click.secho("Running test job for accessing file {}".format(location))
    click.secho(
        "Note: if the image {}:{} is not yet available locally, it will be pulled".format(
            image, tag
        )
    )
    click.secho("-" * 20)
    if os.path.exists(testingdir):
        shutil.rmtree(testingdir)

    run_sync_packtivity(
        testingdir,
        {"spec": testspec, "toplevel": os.getcwd(), "parameters": {}},
        backend=backend,
    )

    with open("{}/_packtivity/packtivity_syncbackend.run.log".format(testingdir)) as f:
        logfile = f.read()

    kerberos_ok = "krbtgt/CERN.CH@CERN.CH" in logfile
    if kerberos_ok:
        principal = re.search("Default principal: (.*@CERN.CH)", logfile).group(1)
    access_ok = "IsReadable" in logfile

    click.secho("-" * 20)
    click.secho("Kerberos: {} {}".format("ok" if kerberos_ok else "not ok", principal))
    click.secho("Access: {}".format("ok" if access_ok else "not ok"))


@auth.command()
@click.argument("location")
def use(location):
    click.secho(
        "export {}={}".format(envvar["auth_location"], os.path.abspath(location))
    )
