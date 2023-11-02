from flask import Flask, render_template
from services import search_ratings

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def main():
    return render_template("index.html")


@app.route("/search/<topic>")
def search(topic):
    results = search_ratings(topic)
    return {
        "results": results,
        "length": len(results)
    }


if __name__ == '__main__':
    app.run(debug=True)

