"""
# query_google_big_query.py
# 
# script to test querying of BigQuery
# 
# https://pypi.python.org/pypi/google-cloud-bigquery
# https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/usage.html
# https://developers.google.com/accounts/docs/application-default-credentials
# 
# https://stackoverflow.com/questions/45003833/how-to-run-a-bigquery-query-in-python
# https://github.com/rajnish4dba/GoogleBigQuery_Scripts/blob/master/ExportDataFromBigQuery.sh
# https://stackoverflow.com/questions/tagged/google-bigquery
# 
"""

import sys, os, time, csv
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.cloud.bigquery import Dataset

DATA_DIR=os.environ['MY_DATA_DIR']

myquery = ("""
    SELECT ...
    FROM ...
    where ...
    group by ...
    order by ...
""")

client = bigquery.Client()
res = client.run_sync_query(myquery)
res.run()

mycols = ['my_id','my_type','my_code','my_total']
df = pd.DataFrame(res.rows, columns=mycols)

fname = DATA_DIR + "/tab_big_query.csv"
print("writing to file", fname)
df.to_csv(fname, sep=',', header=True, index=False)

