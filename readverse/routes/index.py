from flask import Blueprint, Response, render_template, request
from readverse.dto import SearchQueryDTO
from readverse.utils import validate
from readverse.models import db, Story
from sqlalchemy import desc
from datetime import datetime

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("/")
def index():
    recent_stories = db.session.query(Story).order_by(desc(Story.created_at)).all()
    return render_template("pages/index.html", recent_stories=recent_stories)


@bp.get("/search")
@validate
def search(query: SearchQueryDTO):
    # TODO: Search stories based on query
    return render_template("pages/search.html")
