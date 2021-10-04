# RECAST for ATLAS

[![CI](https://github.com/recast-hep/recast-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/recast-hep/recast-atlas/actions/workflows/ci.yml?query=branch%3Amaster)
[![PyPI version](https://badge.fury.io/py/recast-atlas.svg)](https://badge.fury.io/py/recast-atlas)

ATLAS tools to facilitate integration of ATLAS anlayses into RECAST

## Gettting Started

### Install

This package is installable via the standard Python package management tools. E.g.:

```
python -m pip install recast-atlas
```

### Running RECAST

The `recast` tool aims to enable both local execution as well as asynchronous execution on  a [REANA](http://reana.io) cluster. Via the 

#### Locally:

```
recast run examples/rome --backend local
```

#### ...and on REANA

```
recast run examples/rome --backend reana
```



(On LXPLUS)

```
ssh http://lxplus-cloud.cern.ch
source ~recast/public/setup.sh
recast catalogue ls
recast run examples/rome
```
