from setuptools import setup, find_packages
from os import path
import sys

this_directory = path.abspath(path.dirname(__file__))
if sys.version_info.major < 3:
    from io import open
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as readme_md:
    long_description = readme_md.read()

setup(
  name = 'recast-atlas',
  version = '0.0.18',
  description = 'RECAST for ATLAS at the LHC',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  package_dir={'': 'src'},
  packages=find_packages(where='src'),
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
      'black'
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
)
