from setuptools import setup

extras_require = {
    'develop': {'pytest', 'flake8>=3.9.0', 'black'},
    'local': [
        'yadage>=0.21.0',  # yadage[viz] breaks so install following manually
        'adage',  # compatible versions controlled through yadage
        'packtivity',  # compatible versions controlled through yadage
        'pydotplus==2.0.2',
        'pydot',  # from yadage[viz] extra
        'pygraphviz',  # from yadage[viz] extra
    ],
    'kubernetes': ['kubernetes>=9.0.0'],
    'reana': ['reana-client>=0.8.0'],
}

setup(extras_require=extras_require)
