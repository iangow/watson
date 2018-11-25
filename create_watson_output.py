#!/usr/bin/env python3
# -*- coding: utf-8 -*-
conn_string = "postgresql://aaz2.chicagobooth.edu:5432/postgres"

import pandas as pd
import json 
from sqlalchemy import create_engine

from watson import extract_scores, expand_json

db_engine = create_engine(conn_string)

sql = """
    SELECT company_id, executive_id, file_name, profile
    FROM big5.watson_output_raw
    INNER JOIN big5.watson_input
    USING (hash)
    """
    
df = pd.read_sql(sql, db_engine)

df['scores'] = df['profile'].map(lambda x: extract_scores(x))
df_mod = expand_json(df.drop(['profile'], axis=1), 'scores')

df_mod.to_sql("watson_output_alt", db_engine, "big5", 
              if_exists = 'replace', index = False)
