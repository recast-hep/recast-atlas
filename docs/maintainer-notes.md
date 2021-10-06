# Notes for maintainers

## Making a new release

To make a new release of `recast-atlas` a maintainer should execute the following workflow:

1. Verify that you're on the project default branch and are synced with GitHub

```console
$ git checkout master && git pull
```

2. Use `bump2version` to bump the version and create a commit and tag

```console
$ bump2version <part>
```

3. Push the commit and the tag to GitHub, triggering a distribution to be built and published to [TestPyPI](https://test.pypi.org/project/recast-atlas/).

```console
$ git push origin master --tags
```

4. Got to [TestPyPI](https://test.pypi.org/project/recast-atlas/) to check that the release page looks okay. If you want to verify that the sdist and wheel are valid you can either download them manually or with

```console
$ python -m pip download --extra-index-url https://test.pypi.org/simple/ --pre recast-atlas
```

or you can install them with

```console
$ python -m pip install --upgrade --extra-index-url https://test.pypi.org/simple/ --pre recast-atlas
```

to perform local tests.

5. Once satisfied with the TestPyPI version, a release can be made through GitHub. Go to the project releases page: https://github.com/recast-hep/recast-atlas/releases

6. Click "Draft a new release".

7. On the new page enter the tag you just pushed (e.g. `v0.1.0`) in the "Tag version" box and the "Release title" box (to make it easy unless you really want to get descriptive).

8. Enter any release notes and click "Publish release".
   * This then kicks of the publication CD workflow that will use the PyPI API key to publish.
