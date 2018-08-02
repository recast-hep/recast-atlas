import os
import yaml

def extract_results(resultspec, runspec, backend):
    assert backend == 'local'
    results = []
    for r in resultspec:
        results.append(
            {'name': r['name'], 'value': yaml.load(open(os.path.join(runspec['dataarg'],r['relpath'])))}
        )
    return results
