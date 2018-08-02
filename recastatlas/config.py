class Config(object):
    @property
    def catalogue(self):
        return {
            'examples/rome': {
                'metadata': {
                    'short_description': 'Example from ATLAS Exotics Rome Workshop 2018',
                    'author': 'Lukas Heinrich',
                    'input requirements': '',
                },
                'example_inputs': {
                    'default': ''
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
                    'default': ''
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
                    'default': ''
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
