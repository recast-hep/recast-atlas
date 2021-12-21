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

### Running RECAST

The `recast` tool aims to enable both local execution as well as asynchronous execution on a [REANA](http://reana.io) cluster. Via the

#### Locally:

```
recast run examples/rome --backend local
```

#### ...and on REANA

```
recast run examples/rome --backend reana
```

#### On [LXPLUS8](https://clouddocs.web.cern.ch/clients/lxplus.html)

```console
ssh lxplus8.cern.ch
source ~recast/public/setup.sh
recast catalogue ls
recast run examples/rome
```
