# Contributing to the RECAST CLI

`recast` is meant to be a convenience tool for analysts within collaboration. We welcome contributions
from the community to improve the user experience.


## Development install

```
python -m pip install -e '.[develop,local,snakemake]'
```

## Running unit tests

We use `pytest` as a unit testing framework

```
pytest tests
```

## Smoke Testing the `local` backend

```
recast run testing/busyboxtest --backend docker
```

## Smoke Testing the `docker` backend

```
docker build -f docker/Dockerfile -t recastestimg .
RECAST_DOCKER_IMAGE=recastestimg recast run testing/busyboxtest --backend docker
```

## Smoke Testing Snakemake workflows

```
recast run examples/snakehello --backend local
RECAST_DOCKER_IMAGE=recastestimg recast run examples/snakehello --backend docker
RECAST_DOCKER_IMAGE=recastestimg RECAST_SNAKEMAKE_SDM=apptainer recast run testing/snakecontainertest --backend docker
```

The Snakemake-in-docker integration test is opt-in:
`RECAST_TEST_DOCKER_IMAGE=recastestimg pytest tests/test_snakemake.py`
