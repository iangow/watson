#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

from sqlalchemy import create_engine

conn_string = "postgresql://aaz.chicagobooth.edu:5432/postgres"

def get_input():
    db_engine = create_engine(conn_string)
    
    # obtaining texts
    print('Querying the database for texts...')
    print('Creating the database connection...')
    
    print('Obtaining texts from the database...')
    sql_input = """
        SELECT hash, text
        FROM personality.watson_input
        -- LIMIT 5
        WHERE hash NOT IN (SELECT hash FROM personality.watson_output_raw)
    """
    #%%
    
    texts = pd.read_sql(sql_input, db_engine)
    if not len(texts):
        Exception('Error: no records were returned by the SQL query.')
    if not 'text' in texts:
        Exception('Error: The resulting table has no column "text".')
    print('{0} records are returned.'.format(len(texts)))
    db_engine.dispose() # obtaining texts can be long enough for the connection to timeout
    db_engine = None
    return texts 

texts = get_input()

if texts.shape[0] > 0:
    from personalityinsights import PersonalityInsights as PI
    pi = PI()
    texts['profile'] = texts['text'].map(lambda x: pi.get_profile(x))
    
    db_engine = create_engine(conn_string)
    df = texts.drop(['text'], axis=1)
    df.to_sql("watson_output_raw", db_engine, "personality", if_exists = 'append', index = False)
