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
    'pyyaml',
    'yadage-schemas==0.10.6',
  ],
  extras_require =  {
    'local': [
      'yadage==0.19.9',
      'packtivity==0.14.13'
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
  ]
)
