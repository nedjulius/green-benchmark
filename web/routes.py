from flask import Blueprint, request, render_template
from services import search_ratings


routes = Blueprint('routes', __name__)


@routes.route("/", methods=["GET"])
@routes.route("/index", methods=["GET"])
def index():
    topic = request.args.get('topic', '')
    results = search_ratings(topic)
    return render_template("search.html", topic=topic, results=results)


@routes.route("/api/search", methods=["GET"])
def search():
    topic = request.args.get('topic', '')
    results = search_ratings(topic)
    return {
        "results": results,
        "length": len(results)
    }