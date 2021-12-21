# RECAST for ATLAS

[![CI](https://github.com/recast-hep/recast-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/recast-hep/recast-atlas/actions/workflows/ci.yml?query=branch%3Amain)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/recast-hep/recast-atlas/main.svg)](https://results.pre-commit.ci/latest/github/recast-hep/recast-atlas/main)
[![PyPI version](https://badge.fury.io/py/recast-atlas.svg)](https://badge.fury.io/py/recast-atlas)

ATLAS tools to facilitate integration of ATLAS analyses into RECAST

## Getting Started

### Install

`recast-atlas` is installable from PyPI using `pip` inside of your Python virtual environment

```
python -m pip install recast-atlas
```

### CLI API

The `recast-atlas` CLI API:

```
$ recast --help
Usage: recast [OPTIONS] COMMAND [ARGS]...

Options:
  -l, --loglevel TEXT
  --help               Show this message and exit.

Commands:
  auth       Authentication Commands (to gain access to internal data)
  backends   The RECAST computational backends.
  catalogue  The RECAST Analysis Catalogue
  ci         Helper Commands for CI systems
  retrieve   Retrieve RECAST Results from asynchronous submissions
  run        Run a RECAST Workflow synchronously
  software   Build Container Images for RECAST
  status     Get the Status of a asynchronous submission
  submit     Submit a RECAST Workflow asynchronously
  tests      Run a test
```

### Running RECAST

`recast-atlas` aims to enable both local execution as well as asynchronous execution on a [REANA](http://reana.io) cluster.

#### Local backend

Running the example from the [ATLAS Exotics Rome Workshop 2018][ATLAS Exotics Workshop 2018] using the `local` backend:

```
recast run examples/rome --backend local
```

#### REANA cluster backend

Running the example from the [ATLAS Exotics Rome Workshop 2018][ATLAS Exotics Workshop 2018] using the `reana` backend:

```
recast run examples/rome --backend reana
```

[ATLAS Exotics Workshop 2018]: https://indico.cern.ch/event/710748/contributions/2982534/subcontributions/254796

#### On [LXPLUS8](https://clouddocs.web.cern.ch/clients/lxplus.html)

```console
ssh lxplus8.cern.ch
source ~recast/public/setup.sh
recast catalogue ls
recast run examples/rome
```
