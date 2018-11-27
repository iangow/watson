#!/usr/bin/env python3
# -*- coding: utf-8 -*-
conn_string = "postgresql://aaz2.chicagobooth.edu:5432/postgres"

import pandas as pd
import json 
from sqlalchemy import create_engine
from datetime import datetime as dt
from watson import extract_scores, expand_json

db_engine = create_engine(conn_string)
db_schema = "big5"
db_table = "watson_output"

sql = """
    SELECT company_id, executive_id, file_name, profile
    FROM big5.watson_output_raw
    INNER JOIN big5.watson_input
    USING (hash)
    """
    
df = pd.read_sql(sql, db_engine)

df['scores'] = df['profile'].map(lambda x: extract_scores(x))
df_mod = expand_json(df.drop(['profile'], axis=1), 'scores')

df_mod.to_sql(db_table, db_engine, schema = db_schema, 
              if_exists = 'replace', index = False)

# Add table comment              
db_comment = 'CREATED USING GitHub:iangow/watson/watson.py ON ' + \
              dt.utcnow().strftime('%Y-%m-%d %T UTC') + '.'

sql = "COMMENT ON TABLE " + db_schema  + "." + db_table + " IS '" + db_comment + "';"
connection = db_engine.connect()
trans = connection.begin()
connection.execute(sql)
trans.commit()
connection.close()

# Fix permissions
sql = 'ALTER TABLE '  + db_schema  + "." + db_table + ' OWNER TO ' + db_schema
db_engine.execute(sql)
sql = 'GRANT SELECT ON '  + db_schema  + "." + db_table + ' TO ' + db_schema + '_access'
db_engine.execute(sql)
