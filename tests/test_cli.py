from click.testing import CliRunner
from recastatlas.cli import recastatlas
from recastatlas.subcommands.run import run

def test_cli():
    runner = CliRunner()
    test = runner.invoke(recastatlas)
    assert test.exit_code == 0

def test_run_hello_world():
    runner = CliRunner()
    test = runner.invoke(run,['testing/busyboxtest','--backend','local'])
    assert test.exit_code == 0