from flask import Blueprint, Response, render_template, request
from readverse.dto import SearchQueryDTO

from readverse.utils import validate


bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("/")
def index():
    # TODO: Logic to get all recently created stories
    return render_template("pages/index.html")


@bp.get("/search")
@validate
def search(query: SearchQueryDTO):
    # TODO: Search stories based on query
    return render_template("pages/search.html")
