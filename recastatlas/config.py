class Config(object):
    @property
    def backends(self):
        return {
            'local': {
                'metadata': {
                    'short_description': 'runs locally'
                },
                'fromstring': 'multiproc:auto'
            },
            'kubernetes': {
                'metadata': {
                    'short_description': 'runs on a Kubernetes cluster'
                }
            }
        }
    @property
    def catalogue(self):
        return {
            'atlas/atlas-conf-2018-041': {
                'metadata': {
                    'short_description': 'ATLAS MBJ',
                },
                'example_inputs': {
                    'default': {
                        'initdata': {
                            'databkgcache': 'cache.root',
                            'weightfiles': ['mc16a_weights.json', 'mc16d_weights.json'],
                            'did': 375893,
                            'inputdata_xrootd': 'root://eosuser.cern.ch//eos/project/r/recast/atlas/ATLAS-CONF-2018-041/testdata/signal_evsel_inputs',
                            'mc16a_pattern': 'r9364',
                            'mc16d_pattern': 'r10201'
                        },
                        'dataopts': {
                            'inputarchive': 'https://gitlab.cern.ch/api/v4/projects/recast-atlas%2Fsusy%2FATLAS-CONF-2018-041/repository/archive.zip?sha=master',
                            'archivematch': '*/examples/inputdata/'
                        }
                    }
                },
                'spec': {
                    'toplevel': 'gitlab-cern:recast-atlas/susy/ATLAS-CONF-2018-041:specs',
                    'workflow': 'workflow.yml',
                }
            },
            'examples/rome': {
                'metadata': {
                    'short_description': 'Example from ATLAS Exotics Rome Workshop 2018',
                    'author': 'Lukas Heinrich',
                    'input requirements': '',
                },
                'example_inputs': {
                    'default': {
                        'initdata': {
                        "dxaod_file": "https://recastwww.web.cern.ch/recastwww/data/reana-recast-demo/mc15_13TeV.123456.cap_recast_demo_signal_one.root",
                        "did": 404958,
                        "xsec_in_pb": 0.00122
                        }
                    },
                    'newsignal': {
                        "initdata": {
                            "did": 404951,
                            "xsec_in_pb": 0.001735,
                            "dxaod_file": "https://recastwww.web.cern.ch/recastwww/data/reana-recast-demo/mc15_13TeV.789012.cap_recast_demo_signal_two.root"
                        }
                    }
                },
                'spec': {
                  "toplevel": "github:reanahub/reana-demo-atlas-recast",
                  "workflow": "workflow/workflow.yml"
                },
                'results': [
                    {'name': 'CLs 95% based upper limit on poi', 'relpath': 'statanalysis/fitresults/limit_data.json'},
                    {'name': 'CLs 95% at nominal poi', 'relpath': 'statanalysis/fitresults/limit_data_nomsignal.json'}
                ]
            },
            'examples/checkmate1': {
                'metadata': {
                    'short_description': 'CheckMate Tutorial Example (Herwig + CM1)',
                    'author': 'Lukas Heinrich',
                    'input requirements': '',
                },
                'example_inputs': {
                    'default': {
                        'initdata': {}
                    }
                },
                'spec': {
                  "toplevel": "github:lukasheinrich/yadage-workflows:phenochain/checkmate_workflow",
                  "workflow": "checkmate_lxplus.yml"
                },
                'results': [
                    {'name': 'CLs 95% at nominal poi', 'relpath': 'downstream/format_results/limits.json'}
                ]

            },
            'examples/checkmate2': {
                'metadata': {
                    'short_description': 'CheckMate Tutorial Example (Herwig + CM2)',
                    'author': 'Lukas Heinrich',
                    'input requirements': '',
                },
                'example_inputs': {
                    'default': {
                        'initdata': {}
                    }
                },
                'spec': {
                  "toplevel": "github:lukasheinrich/yadage-workflows:phenochain/checkmate_workflow",
                  "workflow": "checkmate2_lxplus.yml"
                },
                'results': [
                    {'name': 'CLs 95% at nominal poi', 'relpath': 'downstream/checkmate/checkmaterun/recast/result.txt'}
                ]

            }
        }

config = Config()
