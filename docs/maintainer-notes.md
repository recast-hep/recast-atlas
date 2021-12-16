# Notes for maintainers

## Making a new release

A release requires:
* A Git tag of the code to be released
* A GitHub release to use for future reference
* Building and distributing artifacts of the release (e.g., Python sdist and wheel to PyPI)

To make a new release of `recast-atlas` a maintainer should execute the following workflow:

### Make a Git tag...

#### ...through GitHub Actions

0. Ensure that a maintainer has a [GitHub personal access token][GitHub PAT] saved under the [project's Actions secrets](https://github.com/recast-hep/recast-atlas/settings/secrets/actions) called `ACCESS_TOKEN`.
   - Note that personal access tokens have a lifetime of up to one year, and so the maintainers will be responsible for keeping them updated.

1. Go to the GitHub Actions tab and select the [Bump version workflow][bump version workflow].

2. Click the "Run workflow" button and enter in the Semver part that you want to bump to (major, minor, or patch).

3. Click "Run workflow". This will run `bump2version` with the part that you gave as input and then push the resulting commit and tag to the project repository.
This will trigger a distribution to be built and published to [TestPyPI][TestPyPI].

[GitHub PAT]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
[bump version workflow]: https://github.com/recast-hep/recast-atlas/actions/workflows/bump-version.yml
[TestPyPI]: https://test.pypi.org/project/recast-atlas/

#### ...locally

1. Verify that you're on the project default branch and are synced with GitHub

```console
$ git checkout main && git pull
```

2. Use `bump2version` to bump the version and create a commit and tag

```console
$ bump2version <part>
```

3. Push the commit and the tag to GitHub, triggering a distribution to be built and published to [TestPyPI][TestPyPI].

```console
$ git push origin main --follow-tags
```

### Make a GitHub release from the tag

1. Got to [TestPyPI](https://test.pypi.org/project/recast-atlas/) to check that the release page looks okay. If you want to verify that the sdist and wheel are valid you can either download them manually or with

```console
$ python -m pip download --extra-index-url https://test.pypi.org/simple/ --pre recast-atlas
```

or you can install them with

```console
$ python -m pip install --upgrade --extra-index-url https://test.pypi.org/simple/ --pre recast-atlas
```

to perform local tests.

2. Once satisfied with the TestPyPI version, a release can be made through GitHub. Go to the project releases page: https://github.com/recast-hep/recast-atlas/releases

3. Click "Draft a new release".

4. On the new page enter the tag you just pushed (e.g. `v0.1.0`) in the "Tag version" box and the "Release title" box (to make it easy unless you really want to get descriptive).

5. Enter any release notes and click "Publish release".
   * This then kicks of the publication CD workflow that will use the PyPI API key to publish.

## Deployment to [LXPLUS8](https://clouddocs.web.cern.ch/clients/lxplus.html)

When a new release of `recast-atlas` is out the maintainers should open a PR to produce a new deployment `requirements.txt` at `deploy/recast-atlas-x.y.z-requirements.txt`.
This should be done by unpinning everything, installing the requirements into a Python virtual environment, and then using `python -m pip freeze` to determine the versions that things should be pinned at for deployment.
The resulting `requirements.txt` file should be uploaded to LXPLUS8 under `~recast/deploy/`.

Following that, the deployment script should get updated to the new version release

```console
sed -i 's/<previous-version>/<new-version>/g' deploy/deploy_lxplus8.sh
```

and then uploaded to LXPLUS8 under `~recast/deploy/`.
