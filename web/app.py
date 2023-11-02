from flask import Flask, request, render_template
from services import search_ratings

app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    topic = request.args.get('topic', '')
    results = search_ratings(topic)
    return render_template("search.html", topic=topic, results=results)


@app.route("/api/search", methods=["GET"])
def search():
    topic = request.args.get('topic', '')
    results = search_ratings(topic)
    return {
        "results": results,
        "length": len(results)
    }


if __name__ == '__main__':
    app.run(debug=True)

