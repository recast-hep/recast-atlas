import click
import logging
import yaml
import uuid
import json

from ..config import config
from ..backends import run_sync, run_async, check_async
from ..resultsextraction import extract_results

log = logging.getLogger(__name__)


def make_spec(name, data, inputs):
    spec = {
        "dataarg": name,
        "dataopts": inputs.get("dataopts", {}),
        "initdata": inputs["initdata"],
        "workflow": data["spec"]["workflow"],
        "toplevel": data["spec"]["toplevel"],
        "visualize": True,
    }
    return spec


@click.command(help="Run a RECAST Workflow synchronously")
@click.argument("name")
@click.argument("inputdata", default="")
@click.option("--example", default="default")
@click.option("--backend", type=click.Choice(["local", "docker"]), default=config.default_run_backend)
@click.option("--tag", default=None)
@click.option("--format-result/--raw", default=True)
def run(name, inputdata, example, backend, tag, format_result):
    data = config.catalogue[name]
            
    if inputdata:
        inputs = yaml.safe_load(open(inputdata))
    else:
        try:
            inputs = data["example_inputs"][example]
        except:
            raise click.ClickException(
                "Example '{}' not found. Choose from {}".format(
                    example, list(data.get("example_inputs", {}).keys())
                )
            )

    instance_id = "recast-{}".format(tag or str(uuid.uuid1()).split("-")[0])
    spec = make_spec(instance_id, data, inputs)

    try:
            run_sync(name, spec, backend=backend)
    except:
        log.exception("caught exception")
        exc = click.exceptions.ClickException(
            click.style("Workflow failed", fg="red")
        )
        exc.exit_code = 1
        raise exc


    log.info("RECAST run finished.")

    if not "results" in data:
        log.info(
            "No result file specified in config. Check out workdir for {} manually".format(
                instance_id
            )
        )
        return

    result = extract_results(data["results"], spec["dataarg"], backend=backend)
    if not format_result:
        click.echo(json.dumps(result))
    else:
        formatted_result = yaml.safe_dump(result, default_flow_style=False)
        click.secho(
            "\nRECAST result {} {}:\n--------------\n{}".format(
                name, instance_id, formatted_result
            )
        )

@click.command(help="Submit a RECAST Workflow asynchronously")
@click.argument("name")
@click.argument("inputdata", default="")
@click.option("--example", default="default")
@click.option("--infofile", default=None)
@click.option("--tag", default=None)
@click.option("--backend", type = click.Choice(['kubernetes','reana']))
def submit(name, inputdata, example, infofile, tag, backend):
    analysis_id = name
    data = config.catalogue[analysis_id]
    if inputdata:
        inputs = yaml.safe_load(open(inputdata))
    else:
        try:
            inputs = data["example_inputs"][example]
        except:
            raise click.ClickException(
                "Example '{}' not found. Choose from {}".format(
                    example, list(data.get("example_inputs", {}).keys())
                )
            )

    instance_id = "recast-{}".format(tag or str(uuid.uuid1()).split("-")[0])
    spec = make_spec(instance_id, data, inputs)

    submission = run_async(instance_id, spec, backend=backend)

    click.secho("{} submitted".format(str(instance_id)))
    if infofile:
        with open(infofile, "w") as info:
            json.dump({"analysis_id": analysis_id, "instance_id": instance_id, 'submission': submission}, info)

@click.command(help="Get the Status of a asynchronous submission")
@click.option("--infofile", default=None)
@click.option("--backend", type = click.Choice(['kubernetes','reana']))
def status(infofile, backend):
    submission = json.load(open(infofile))
    instance = submission['instance_id']
    status = check_async(submission, backend=backend)
    click.secho("{}\t{}".format(instance, status["status"]))

@click.command(help="Retrieve RECAST Results from asynchronous submissions")
@click.option("--name", default=None)
@click.option("--instance", default=None)
@click.option("--infofile", default=None)
@click.option("--show-url/--no-url", default=False)
@click.option("--tunnel/--no-tunnel", default=False)
@click.option("--format-result/--raw", default=True)
def retrieve(infofile, name, instance, show_url, tunnel, format_result):
    raise NotImplementedError
    backend = "kubernetes"
    if show_url:
        from kubernetes import client as k8client
        from kubernetes import config as k8config

        k8config.load_kube_config()
        port = 30000

        tunnel_host = "lxplus.cern.ch"

        host = "{}".format(
            k8client.CoreV1Api().list_node().to_dict()["items"][0]["metadata"]["name"]
        )

        if tunnel:
            ssh_cmd = "ssh -fNL {}:{}:{} {}".format(port, host, port, tunnel_host)
            click.secho(ssh_cmd)
            host = "127.0.0.1"
        else:
            host = host + ".cern.ch"
        click.secho(
            "http://{host}:{port}/{name}".format(host=host, port=port, name=instance)
        )
        return
    data = config.catalogue[name]
    if not "results" in data:
        log.info(
            "No result file specified in config. Check out workdir for {} manually".format(
                name
            )
        )
        return
    result = extract_results(data["results"], instance, backend=backend)
    if not format_result:
        click.echo(json.dumps(result))
    else:
        formatted_result = yaml.safe_dump(result, default_flow_style=False)
        click.secho(
            "\nRECAST result {} {}:\n--------------\n{}".format(
                name, instance, formatted_result
            )
        )
