import json
import pandas as pd

def get_scores(d):
    '''
    Extracts scores from a dictionary
    :param d: The dictionary or subdictionary returned by the IBM Watson Personality Insights service
    :return: A dictionary containing the extracted scores in a format suitable for writing to a database
    '''
    for key in [ 'trait_id', 'percentile', 'raw_score', 'significant' ]:
        if not key in d:
            Exception('Error: The provided dictionary has no key "' + key + '".')
    score_title = d['trait_id']
    return {
        score_title + '_pc': d['percentile'],
        score_title + '_raw': d['raw_score'],
        score_title + '_sig': d['significant']
    }

def extract_scores(profile):
    scores = { 'word_count': 0 }
    if not 'error' in profile:
        if 'word_count' in profile:
            scores['word_count'] = profile['word_count']
        for category_name in [ 'personality', 'needs', 'values' ]:
            if not category_name in profile:
                continue
            for category in profile[category_name]:
                scores = { **scores, **get_scores(category) }
                if 'children' in category:
                    for child in category['children']:
                        scores = { **scores, **get_scores(child) }
    return json.dumps(scores)

def expand_json(df, col):
    return pd.concat([df.drop([col], axis=1),
                      df[col].map(lambda x: json.loads(x)).apply(pd.Series)], axis=1)
