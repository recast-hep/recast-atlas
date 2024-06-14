# RECAST for ATLAS

[![DOI](https://zenodo.org/badge/142000927.svg)](https://doi.org/10.5281/zenodo.5854896)

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

Run the example from the [ATLAS Exotics Rome Workshop 2018][ATLAS Exotics Workshop 2018] using the `local` backend:

```
python -m pip install --upgrade 'recast-atlas[local]' coolname
```

```
PACKTIVITY_DOCKER_CMD_MOD="-u root" recast run examples/rome --backend local --tag "local-$(coolname 2)"
```

#### REANA cluster backend

Asynchronously run the example from the [ATLAS Exotics Rome Workshop 2018][ATLAS Exotics Workshop 2018] using the `reana` backend:

```
python -m pip install --upgrade 'recast-atlas[reana]' coolname
```

Authenticate to use the REANA cluster
```
# Set these variables to your personal secret values
export RECAST_AUTH_USERNAME="<your RECAST auth username>"
export RECAST_AUTH_PASSWORD="<your RECAST auth password>"
export RECAST_AUTH_TOKEN="<your RECAST auth token>"

eval "$(recast auth setup -a ${RECAST_AUTH_USERNAME} -a ${RECAST_AUTH_PASSWORD} -a ${RECAST_AUTH_TOKEN} -a default)"
eval "$(recast auth write --basedir authdir)"

export REANA_SERVER_URL=https://reana.cern.ch
export REANA_ACCESS_TOKEN="<your RECAST access token>"
```

```
reana_tag="reana-$(coolname 2)"
recast submit examples/rome --backend reana --tag "${reana_tag}"
export REANA_WORKON="recast-${reana_tag}"  # REANA_WORKON is a helper variable that sets workflow automatically
```

Check on the state of the REANA workflow

```
reana-client status
# reana-client status --workflow "<use the created tag>"  # if REANA_WORKON not set
```

Download the results after the workflow succeeds

```
reana-client download --output-directory output
# reana-client download --workflow "<use the created tag>" --output-directory output
```

```
# Clean up the environment of personal information in environmental variables
eval $(recast auth destroy)
```

[ATLAS Exotics Workshop 2018]: https://indico.cern.ch/event/710748/contributions/2982534/subcontributions/254796

#### On [LXPLUS9](https://clouddocs.web.cern.ch/clients/lxplus.html)

```console
ssh lxplus9.cern.ch
source ~recast/public/setup.sh
recast catalogue ls
recast run examples/rome
```
