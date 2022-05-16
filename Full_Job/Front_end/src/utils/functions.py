import pandas as pd
import json

def keggmaps2table(keggmaps):
    result = pd.DataFrame(columns=['name', 'id', 'general category', 'category'])
    for child in keggmaps['children']:
        first_c = child['name']
        gcs = child['children']
        for gc in gcs:
            second_c = gc['name']
            ggcs = gc['children']
            for ggc in ggcs:
                result = result.append({'name': ggc['name'][1],
                                        'id': ggc['name'][0],
                                        'general category': first_c,
                                        'category': second_c
                                        }, ignore_index=True)
    return result

keggmaps = json.load('src/utils/keggMaps.js')
table = keggmaps2table(keggmaps)
table.to_csv('src/utils/keggmaps2table.tsv', sep='\t', index=False)
