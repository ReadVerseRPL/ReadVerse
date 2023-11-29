from flask import Blueprint, Response, render_template, request
from readverse.dto import SearchQueryDTO
from readverse.utils import validate
from readverse.models import db, Story
from sqlalchemy import desc
from datetime import datetime

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("/")
def index():
    # Fetch all recently created stories, ordered by their creation date
    recent_stories = db.session.query(Story).order_by(desc(Story.created_at)).all()

    # TODO: to be delete. 
    # Dummy data for recent stories
    # recent_stories = [
    #     Story(id=1,title="The Mysterious Forest",description="An intriguing tale of adventure and mystery in a mystical forest.",created_at=datetime.now()),
    #     Story(id=2,title="Journey to the Unknown",description="A gripping story of a brave explorer facing the unknown.",created_at=datetime.now()),
    #     Story(id=3,title="The Lost Treasure",description="A thrilling hunt for a long-lost treasure that hides a dark secret.",created_at=datetime.now())
    # ]*3

    # Pass the stories to the template
    return render_template("pages/index.html", recent_stories=recent_stories)


@bp.get("/search")
@validate
def search(query: SearchQueryDTO):
    # TODO: Search stories based on query
    return render_template("pages/search.html")
