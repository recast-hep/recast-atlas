from __future__ import annotations

import getpass
import logging
import os
import string
from distutils.dir_util import copy_tree

try:
    from importlib.resources import files
except ImportError:
    # Support Python 3.8 as importlib.resources added in Python 3.9
    # https://docs.python.org/3/library/importlib.resources.html#importlib.resources.files
    from importlib_resources import files

import click
import yaml

from ..config import config
from ..testing import validate_entry

log = logging.getLogger(__name__)
default_meta = {"author": "unknown", "short_description": "no description", "tags": []}


@click.group(help="The RECAST Analysis Catalogue")
def catalogue():
    pass


@catalogue.command()
@click.argument("name")
def check(name):
    data = config.catalogue[name]
    assert data
    valid = validate_entry(data)
    if not valid:
        click.secho("Sadly something is wrong :(")
    else:
        click.secho("Nice job! Everything looks good.", fg="green")


@catalogue.command()
@click.argument("name")
@click.argument("path")
def create(name, path):
    template_path = files("recastatlas") / "data/templates/helloworld"
    copy_tree(template_path, path)
    recast_file = os.path.join(path, "recast.yml")
    data = string.Template(open(recast_file).read()).safe_substitute(
        name=name, author=getpass.getuser()
    )
    with open(recast_file, "w") as f:
        f.write(data)
    click.secho(
        f"New skeleton created at {path}\nRun $(recast catalogue add {path}) to add to the catlogue"
    )


@catalogue.command()
def paths():
    paths = config.catalogue_paths()
    out = "\n".join(["* " + x for x in paths])
    click.secho("Paths considered by RECAST:\n--------------------------")
    click.secho(out)


@catalogue.command()
@click.argument("path")
def add(path):
    path = os.path.realpath(path)
    if os.path.exists(path) and os.path.isdir(path):
        paths = config.catalogue_paths(include_default=False)
        paths.append(path)
        paths = sorted(list(set(paths)))
        click.secho("export RECAST_ATLAS_CATALOGUE=" + ":".join(paths))
    else:
        log.warning("path %s does not exist or is not a directory", path)
        raise click.Abort()


@catalogue.command()
@click.argument("path")
def rm(path):
    path = os.path.realpath(path)
    paths = config.catalogue_paths(include_default=False)
    filtered_paths = [p for p in paths if p != path]
    filtered_paths = sorted(list(set(filtered_paths)))
    if not filtered_paths:
        click.secho("unset RECAST_ATLAS_CATALOGUE")
    else:
        click.secho("export RECAST_ATLAS_CATALOGUE=" + ":".join(filtered_paths))


@catalogue.command()
def ls():
    fmt = "{0:35}{1:60}{2:20}{3:20}"
    click.secho(fmt.format("NAME", "DESCRIPTION", "EXAMPLES", "TAGS"))

    for k, v in sorted(config.catalogue.items(), key=lambda x: x[0]):
        click.secho(
            fmt.format(
                k,
                v.get("metadata", default_meta)["short_description"],
                ",".join(list(v.get("example_inputs", {}).keys())),
                ",".join(v.get("metadata", default_meta).get("tags", [])),
            )
        )


@catalogue.command()
@click.argument("name")
def describe(name):
    data = config.catalogue[name]
    metadata = data.get("metadata", default_meta)
    toprint = """\

{name:20}
--------------------
description  : {short:20}
author       : {author}
toplevel     : {toplevel}
""".format(
        author=metadata.get("author", "N/A"),
        name=name,
        short=metadata.get("short_description", "N/A"),
        toplevel=data["spec"]["toplevel"],
    )
    click.secho(toprint)


@catalogue.command()
@click.argument("name")
@click.argument("example")
def example(name, example):
    data = config.catalogue[name]
    if example not in data.get("example_inputs", {}):
        click.secho("example not found.")
        return
    click.secho(yaml.dump(data["example_inputs"][example], default_flow_style=False))
