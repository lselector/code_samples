"""
# Working with SQL databases from python
# template for querying Oracle
# Look here:
#  - https://community.oracle.com/thread/4212183
#  - https://stackoverflow.com/questions/35781580/cx-oracle-import-data-from-oracle-to-pandas-dataframe
#  - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html
"""

import pandas as pd
import cx_Oracle

dsn_tns = cx_Oracle.makedsn(ip, port, SID)
connection = cx_Oracle.connect(user, passwd, dsn_tns)

sql = """ select ... from ... where ... """
df = pd.read_sql(sql, con=connection)
df.to_csv(fname, header=True, index=False)

# ---------------------------------------------------------
# or you can switch to pickle files - it is much faster:

import pickle
fname = "junk.pk"
with open(fname, 'wb') as fh:
    pickle.dump(df, fh, protocol=pickle.HIGHEST_PROTOCOL)

# and to read pickle file back:
with open(fname, 'rb') as fh:
    df2 = pickle.load(fh)

