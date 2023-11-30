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
    all_story = db.session.query(Story).all()
    result=[]
    query = query.query
    if 'author=' in query:
        author = query.split('author=')[1].strip()
        for story in all_story:
            if author == story.author.username:
                result.append(story)    
    elif 'description=' in query:
        desc = query.split('description=')[1].strip().lower()
        for story in all_story:
            if desc in story.description.lower():
                result.append(story)
    elif 'genre=' in query:
        genre = query.split('genre=')[1].strip().lower()
        for story in all_story:
            if genre in [genre.lower() for genre in story.genres]:
                result.append(story)
    elif 'rating=' in query:
        rate = query.split('rating=')[1].strip().lower()
        try:
            rate = int(rate)
            for story in all_story:
                if (story.overall_rating if story.overall_rating != None else 0) >= rate:
                    result.append(story)
        except:
            return render_template("pages/search.html", result=result)
    else:
        if 'title=' in query:
            query = query.split('title=')[1].strip()
        query = query.strip().lower()
        for story in all_story:
            if query in story.title.lower():
                result.append(story)

    return render_template("pages/search.html", result=result)
