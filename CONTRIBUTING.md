# Contributing to the RECAST CLI

`recast` is meant to be a convenience tool for analysts within collaboration. We welcome contributions
from the community to improve the user experience.


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

