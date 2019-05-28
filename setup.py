import os
from setuptools import setup, find_packages

setup(
  name = 'recast-atlas',
  version = '0.0.8',
  description = 'RECAST for ATLAS at the LHC',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [
    'click',
    'pyyaml'
  ],
  entry_points = {
      'console_scripts': [
          'recast=recastatlas.cli:recastatlas',
      ],
  },
  dependency_links = [
  ]
)
