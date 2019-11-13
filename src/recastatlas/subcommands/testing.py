import click
import uuid
from ..config import config
from ..testing import run_test, get_shell


@click.group(help="Run a test")
def testing():
    pass


@testing.command()
@click.argument("name")
def ls(name):
    fmt = "{0:10}{1:35}{2:60}"
    click.secho(fmt.format("INDEX", "NAME", "DESCRIPTION"))

    data = config.catalogue[name]
    tests = data.get("tests", [])

    for i, t in enumerate(tests):
        click.secho(
            fmt.format(
                str(i).ljust(10),
                t.get("name", "NO NAME"),
                t.get("description", "NO DESC"),
            )
        )


@testing.command(help="Run a test")
@click.argument("name")
@click.argument("testname")
@click.option("--backend", type=click.Choice(["local", "docker"]), default = config.default_run_backend)
@click.option("--tag", default=None)
def run(name, testname, backend, tag):
    data = config.catalogue[name]
    testdict = {t.pop("name"): t for t in data["tests"]}
    for k, v in testdict.items():
        if not "toplevel" in v:
            v["toplevel"] = data["spec"]["toplevel"]

    instance_id = "recast-test-{}".format(tag or str(uuid.uuid1()).split("-")[0])

    spec = testdict[testname]
    success = run_test(instance_id, spec, backend=backend)
    if not success:
        click.secho("test {} failed".format(testname), fg="red")
        raise click.Abort()
    click.secho("test {} succeeded".format(testname), fg="green")


@testing.command(help="Run a test")
@click.argument("name")
@click.argument("testname")
@click.option("--backend", type=click.Choice(["local", "docker"]), default=config.default_run_backend)
@click.option("--tag", default=None)
def shell(name, testname, backend, tag):
    data = config.catalogue[name]
    testdict = {t.pop("name"): t for t in data["tests"]}
    for k, v in testdict.items():
        if not "toplevel" in v:
            v["toplevel"] = data["spec"]["toplevel"]

    instance_id = "recast-testshell-{}".format(tag or str(uuid.uuid1()).split("-")[0])
    spec = testdict[testname]
    print(get_shell(instance_id, spec, backend=backend))
