from flask import Flask, g
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)


# close db connection
@app.teardown_appcontext
def close_connection(exception):
  print(exception)
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()


if __name__ == '__main__':
    app.run(debug=True)

