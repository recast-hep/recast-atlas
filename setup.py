from setuptools import setup

extras_require = {
    'develop': {'pytest', 'flake8>=3.9.0', 'black'},
    'local': ['packtivity>=0.14.23', 'yadage[viz]>=0.20.2'],
    'kubernetes': ['kubernetes==9.0.0'],
    'reana': ['reana-client>=0.8.0'],
}

setup(extras_require=extras_require)
