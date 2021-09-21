from setuptools import setup

extras_require = {
    'develop': {'pytest', 'flake8>=3.9.0', 'black'},
    'local': [
        'pydotplus==2.0.2',
        'adage==0.10.1',
        'yadage-schemas==0.10.6',
        'packtivity==0.14.23',
        'yadage==0.20.1',  # yadage[viz] breaks so install following manually
        'pydot',  # from yadage[viz] extra
        'pygraphviz',  # from yadage[viz] extra
    ],
    'kubernetes': ['kubernetes==9.0.0'],
    'reana': [
        'setuptools<58.0.0',  # c.f. https://github.com/reanahub/reana-client/issues/558
        'reana-client==0.7.5',
    ],
}

setup(extras_require=extras_require)
