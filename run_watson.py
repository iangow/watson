#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
from os import getenv

pghost = getenv("PGHOST")
pgdatabase =  getenv("PGDATABASE")
conn_string = "postgresql://" + pghost + ":5432/" + pgdatabase

def get_input():
    db_engine = create_engine(conn_string)
    
    # obtaining texts
    print('Querying the database for texts...')
    print('Creating the database connection...')
    
    print('Obtaining texts from the database...')
    sql_input = """
        SELECT hash, text
        FROM big5.watson_input_agg
        UNION 
        SELECT hash, text
        FROM big5.watson_input
        WHERE hash NOT IN (SELECT hash FROM big5.watson_output_raw)
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

if __name__=="__main__":
    texts = get_input()

    if texts.shape[0] > 0:
        from personalityinsights import PersonalityInsights as PI
        pi = PI()
        texts['profile'] = texts['text'].map(lambda x: pi.get_profile(x))

        db_engine = create_engine(conn_string)
        df = texts.drop(['text'], axis=1)
        df.to_sql("watson_output_raw", db_engine, "big5", if_exists = 'append', index = False)
