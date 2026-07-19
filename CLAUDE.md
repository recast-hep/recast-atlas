# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this package is

`recast-atlas` is the RECAST CLI for ATLAS: it re-executes preserved LHC analyses ("workflows") against new physics-model inputs to produce results such as CLs values. The default workflow engine is **yadage** (parametrized DAGs of containerized steps, "packtivities" — see `papers/1706.01878v1.pdf`), around whose ecosystem (`yadage`, `packtivity`, `adage`, `yadage-schemas`) this package is a thin orchestration/catalogue/CLI layer. Catalogue entries can alternatively declare a **Snakemake** workflow via `spec.workflow_type: snakemake` (local backend only for now).

## Development setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[develop,local,snakemake]"
uv pip install "setuptools<81"   # yadageschemas needs pkg_resources, removed in setuptools>=81
```

- `develop` extra: pytest, ruff, pre-commit. `local` extra: the yadage stack, needed to actually run yadage workflows (and by the `docker`-backend code paths too, since they import yadage modules). `snakemake` extra: `snakemake>=8` (only installs on Python >= 3.11 via environment marker).
- Build backend is hatchling with hatch-vcs; the version comes from git tags (`src/recastatlas/_version.py` is generated, never edit).

## Common commands

```bash
pytest tests                                   # unit tests (tests/test_cli.py, click CliRunner-based)
pytest tests/test_cli.py -k <name>             # single test
ruff check . && ruff format .                  # lint/format (config in pyproject.toml)
pre-commit run --all-files

# Smoke tests (need Docker running):
recast run examples/rome --backend docker      # full end-to-end example, ~30 s
recast run testing/busyboxtest --backend docker
recast run examples/snakehello --backend local # snakemake path, no Docker needed
```

`recast --help` for the CLI surface. Console script `recast` maps to `recastatlas.cli:recastatlas` (a click group).

## Architecture

The central flow of `recast run <name> --backend <b>`:

1. **Catalogue lookup** — `config.catalogue[name]` (`src/recastatlas/config.py`). The catalogue is built by globbing `*.yml` from the packaged `src/recastatlas/data/catalogue/` plus any `:`-separated dirs in `$RECAST_ATLAS_CATALOGUE`. `process_entry()` fills in `spec.toplevel = <dir-of-yml>/specs` when absent (local workflow resolution). Entry files need `{name, metadata, spec}`; index files (`{name, tags, recast_catalogue_entries}`) recursively include others.
2. **Spec construction** — `make_spec()` in `src/recastatlas/subcommands/run.py` builds the runtime spec dict `{dataarg, dataopts, initdata, workflow, toplevel, visualize}` whose keys are ultimately yadage `run_workflow` kwargs. `dataarg` is the instance id `recast-<tag|uuid>` and doubles as the run/workdir name in cwd. Inputs come from the entry's `example_inputs[<example>]` or a user-supplied YAML file.
3. **Backend dispatch** — `src/recastatlas/backends/__init__.py`. `BACKENDS` dict is populated at import time via try/except-ImportError (missing optional deps silently drop a backend). Sync path (`recast run`): `run_sync()` → `BACKENDS[b].run_workflow(name, spec)` for `local`/`docker`. Async path (`recast submit`/`status`): `run_async()`/`check_async()` → `.submit()`/`.check_workflow()` for `kubernetes`/`reana`.
4. **Results extraction** — `src/recastatlas/resultsextraction.py` reads each `results[].relpath` of the catalogue entry relative to the `dataarg` workdir (engine-agnostic: plain file reads for local/docker, service proxy for kubernetes).

### The backend axis means "where", not "what engine"

The engine is chosen by the catalogue entry (`spec.workflow_type`, default `yadage`); `--backend` chooses where the orchestrator runs. `make_spec` carries `workflow_type` in the spec dict, and backends `pop()` it before dispatching (the yadage `run_workflow(**spec)` call and the docker JSON payload must never see it).

- **snakemake engine** (`src/recastatlas/engines/snakemake.py`): local backend only. Resolves `toplevel` itself (local dir, or `github:org/repo@ref:subpath` via `git clone` into the instance workdir), writes `initdata` as a configfile, and runs the `snakemake` CLI as a subprocess with `--directory <workdir>` so outputs land where results extraction expects. Per-rule environments are Snakemake's job (`container:`/`conda:` + `RECAST_SNAKEMAKE_SDM`); recast adds no per-step container machinery. `run`/`submit` guard against non-local backends with a ClickException; `validate_entry` branches to a `--dry-run` check.

The four backends execute *yadage* workflows; they differ in where the orchestrator runs:

- `local` (`backends/local.py`): yadage in-process (`yadage.steering_api.run_workflow`), packtivity backend from `RECAST_LOCAL_BACKENDSTRING` (default `multiproc:auto`). Each workflow *step* still runs in its own Docker container — "local" only refers to the orchestrator.
- `docker` (`backends/docker.py`): pipes the JSON spec to `yadage-run -f -` inside the `recast/recastatlas` image (env `RECAST_DOCKER_IMAGE`), mounting `/var/run/docker.sock` so steps run as sibling containers.
- `kubernetes` (`backends/kubernetes.py`): POSTs a `yadage.github.io/v1` Workflow CRD (assumes a yadage operator in the cluster).
- `reana` (`backends/reana.py`): compiles the workflow via `yadageschemas.load` and submits `type: yadage` to REANA via `reana-client`.

Backends are duck-typed (no base class): sync backends implement `run_workflow`/`run_packtivity`/`check_backend`, async ones `submit`/`check_workflow`.

### Catalogue entry anatomy

```yaml
name: examples/rome            # <group>/<id>
metadata: {short_description: ..., author: ...}
spec:
  workflow_type: snakemake               # optional; omitted → yadage
  toplevel: github:org/repo@ref:subdir   # or gitlab-cern:..., or omitted → local specs/ dir
  workflow: workflow/workflow.yml        # resolved relative to toplevel (Snakefile path for snakemake)
example_inputs:
  default: {initdata: {...}, dataopts: {...}}
results:
  - {name: ..., relpath: path/under/workdir, load_yaml: true}
```

For yadage, `github:`/`gitlab-cern:` toplevel resolution happens *inside* yadage-schemas (per-file HTTP fetches), not in this package; for snakemake it's a `git clone` in `engines/snakemake.py` (`gitlab-cern:` not yet supported there). Schema validation of workflows (`recast catalogue check`) is in `src/recastatlas/testing.py:validate_entry` — `yadageschemas.load` for yadage, snakemake `--dry-run` for snakemake. The `examples/snakehello` entry (`data/catalogue/examples_snakehello.yml` + `data/catalogue/specs/snakehello/Snakefile`) is the minimal snakemake reference.

### Other subcommands

- `tests` (`subcommands/testing.py`): runs single packtivity steps (not full workflows) declared under a catalogue entry's `tests:` key; `tests shell` drops into a step's environment.
- `auth` (`subcommands/auth.py`): emits shell snippets exporting `RECAST_AUTH_*` credentials; `auth write` materializes them for packtivity (`PACKTIVITY_AUTH_LOCATION`).
- `software` (`subcommands/software.py`): builds analysis container images via docker build or buildkit.
- `retrieve` is `NotImplementedError` (dead code).

### Configuration

Everything is environment-variable driven through the `Config` singleton (`config.py`), values YAML-parsed by `conf_from_env`. Key vars: `RECAST_ATLAS_CATALOGUE`, `RECAST_DEFAULT_RUN_BACKEND` (default `docker`), `RECAST_LOCAL_BACKENDSTRING`, `RECAST_DOCKER_IMAGE`, `RECAST_SNAKEMAKE_CORES` (default `all`), `RECAST_SNAKEMAKE_SDM` (→ `--software-deployment-method`), `REANA_ACCESS_TOKEN`, `YADAGE_SCHEMA_LOAD_TOKEN`, `PACKTIVITY_AUTH_LOCATION`.

## Gotchas

- Ruff config (pyproject.toml) enforces `from __future__ import annotations` as a required import in every module (isort setting); several rule families are intentionally ignored at adoption point — don't "fix" them wholesale.
- Python floor is 3.8 (uses `importlib_resources` fallback); don't introduce syntax/stdlib features beyond that in core code.
- The yadage stack is old and fragile on new Pythons (the `setuptools<81` pin above); the `docker` backend is the most reliable smoke-test path for yadage workflows.
- On Python 3.14, `tests/test_cli.py::test_cli` and `::test_run_hello_world` fail on pristine main (newer click exits 2 on bare invoke; yadage local backend breaks) — don't mistake them for regressions. Similarly `ruff check .` has pre-existing violations when run with a newer ruff than the pre-commit pin; only keep files you touch clean.
- `backends/local.py` imports yadage lazily inside `run_workflow` (so snakemake-only installs work); the `BACKENDS` registry in `backends/__init__.py` swallows ImportError at import time, so keep heavyweight imports out of backend module top level.
