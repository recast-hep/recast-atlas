import os
import json

def extract_results(resultspec, runspec, backend):
    assert backend == 'local'
    results = []
    for r in resultspec:
        results.append(
            {'name': r['name'], 'value': json.load(open(os.path.join(runspec['dataarg'],r['relpath'])))}
        )
    return results
