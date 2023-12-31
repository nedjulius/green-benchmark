from db import query_db

def format_response(entry):
  return {
    'make': entry[0],
    'model': entry[1],
    'engine_size': entry[2],
    'class': entry[3],
    'rating': round(entry[8], 2),
    'description': entry[9]
  }


# This is currently shitty and prone to SQL injections
# We should fix this if we intend to use this in prod lol
# Very primitive escaping and FTS query formatting
def format_fts_query(query):
  return query.replace(' ', '" + "')


def search_ratings(topic=''):
  print(topic)
  if len(topic) == 0:
    return []

  query = 'SELECT * FROM ratings JOIN ratings_fts ON ratings.rowid = ratings_fts.rowid WHERE ratings_fts MATCH ?'
  result = query_db(query, [format_fts_query(topic)])
  print(result)
  if result is None:
    return []
  else:
    # really inefficient now, but we can fix this later
    return list(map(format_response, result))
