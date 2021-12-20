from setuptools import setup

extras_require = {
    'develop': {'pytest', 'flake8>=3.9.0', 'black'},
    'local': [
        'pydotplus==2.0.2',
        'adage>=0.10.1',
        'packtivity>=0.14.23',
        'yadage>=0.20.1',  # yadage[viz] breaks so install following manually
        'pydot',  # from yadage[viz] extra
        'pygraphviz',  # from yadage[viz] extra
    ],
    'kubernetes': ['kubernetes==9.0.0'],
    'reana': ['reana-client>=0.8.0'],
}

setup(extras_require=extras_require)
