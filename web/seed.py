import sqlite3
import sys

sys.path.insert(0, '../scripts')

from create_rating_dataframe import create_rating_dataframe

conn = sqlite3.connect('./db/main.sqlite')

df = create_rating_dataframe()
# write to SQLite full rating database
df.to_sql('ratings', conn, if_exists='replace', index=False)

# create virtual table with full text search FTS5
conn.execute('DROP TABLE IF EXISTS ratings_fts')
conn.execute('CREATE VIRTUAL TABLE ratings_fts USING fts5(make, model)')
# add the makes and models to virtual full text search table
df_fts = df[['make', 'model']].copy()
df_fts.to_sql('ratings_fts', conn, if_exists='append', index=False)

conn.close()
