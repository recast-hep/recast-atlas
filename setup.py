import os
from setuptools import setup, find_packages

def _is_test_pypi():
    """
    Determine if the Travis CI environment has TESTPYPI_UPLOAD defined and
    set to true (c.f. .travis.yml)
    The use_scm_version kwarg accepts a callable for the local_scheme
    configuration parameter with argument "version". This can be replaced
    with a lambda as the desired version structure is {next_version}.dev{distance}
    c.f. https://github.com/pypa/setuptools_scm/#importing-in-setuppy
    As the scm versioning is only desired for TestPyPI, for depolyment to PyPI the version
    controlled through bumpversion is used.
    """
    from os import getenv

    return (
        {'local_scheme': lambda version: ''}
        if getenv('TESTPYPI_UPLOAD') == 'true'
        else False
    )


setup(
  name = 'recast-atlas',
  version = '0.0.16',
  description = 'RECAST for ATLAS at the LHC',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [
    'click',
    'pyyaml',
    'yadage-schemas==0.10.6',
  ],
  extras_require =  {
    'develop': {
      'pytest',
      'pyflakes',
      # 'black'
    },
    'local': [
      'pydotplus==2.0.2',
      'adage==0.9.0',
      'yadage[viz]==0.19.9',
      'packtivity==0.14.20'
    ],
    'kubernetes': [
      'kubernetes==9.0.0'
    ]
  },
  entry_points = {
      'console_scripts': [
          'recast=recastatlas.cli:recastatlas',
      ],
  },
  dependency_links = [
  ],
  use_scm_version=_is_test_pypi(),
)
