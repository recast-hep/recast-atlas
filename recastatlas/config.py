class Config(object):
    @property
    def catalogue(self):
        return {
            'atlas/atlas-conf': {
                'metadata': {
                    'short_description': 'ATLAS MBJ',
                },
                'example_inputs': {
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
                        'data': {
                        "dxaod_file": "https://recastwww.web.cern.ch/recastwww/data/reana-recast-demo/mc15_13TeV.123456.cap_recast_demo_signal_one.root",
                        "did": 404958,
                        "xsec_in_pb": 0.00122
                        }
                    },
                    'newsignal': {
                        "data": {
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
                        'data': {}
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
                        'data': {}
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
