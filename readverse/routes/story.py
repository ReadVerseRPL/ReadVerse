from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from sqlalchemy import select
from readverse.plugins import current_user
from readverse.models import Rating, RegularUser, db, Story
from readverse.dto import CreateCommentDTO, CreateRatingDTO, CreateStoryDTO
from readverse.utils import validate

bp = Blueprint("story", __name__, url_prefix="/story")


@bp.post("/new")
@validate
def create_story(form: CreateStoryDTO):
    genres = form.genres
    if isinstance(genres, str):
        genres = [genres]

    story = Story(
        title=form.title,
        description=form.description,
        content=form.content,
        genres=genres,
        author=current_user,
    )

    db.session.add(story)
    db.session.commit()

    return redirect(url_for("story.read_story", story_id=story.id))


@bp.get("/new")
def create_story_page():
    return render_template("pages/story/new.html")


@bp.get("/<int:story_id>")
def read_story(story_id: int):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()
    if not story:
        abort(404)

    current_rating = None
    if current_user and isinstance(current_user, RegularUser):
        current_rating = db.session.execute(
            select(Rating).where(Rating.author == current_user)
        ).scalar_one_or_none()

    return render_template(
        "pages/story/read.html",
        story=story,
        current_rating=current_rating,
    )


@bp.get("/<int:story_id>/edit")
def edit_story_page(story_id: int):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        abort(404)
        
    return render_template("pages/story/edit.html", story=story)


@bp.post("/<int:story_id>/edit")
@validate
def edit_story(story_id: int, form: CreateStoryDTO):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        abort(404)

    genres = form.genres
    if isinstance(genres, str):
        genres = [genres]

    story.title = form.title
    story.description = form.description
    story.content = form.content
    story.genres = genres

    db.session.commit()

    return redirect(url_for("story.read_story", story_id=story.id))


@bp.get("/<int:story_id>/comments")
def comments(story_id: int):
    # TODO: Get all comments and return as json
    return jsonify(
        {
            "message": "Success",
            "data": [],
        }
    )


@bp.post("/<int:story_id>/comment")
@validate
def create_comment(story_id: int, json: CreateCommentDTO):
    # TODO: Create comment based on content and save, then return json
    content = json.content

    return jsonify(
        {
            "message": "Comment created",
            "data": {},  # TODO: Comment data here
        }
    )


@bp.post("/<int:story_id>/rate")
@validate
def create_rating(story_id: int, json: CreateRatingDTO):

    value = json.value  

    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        abort(404)

    oldRating: Rating = db.session.execute(
        select(Rating).where(Rating.author == current_user)
    ).scalar_one_or_none()

    if ( not oldRating ):
        rating = Rating(
            value = value,
            author = current_user,
            story = story,
        )

        db.session.add(rating)
        db.session.commit()

        return jsonify(
            {
                "message": "Story rated",
                "data": {rating},
            }
        )
    else :
        oldRating.value = value
        db.session.commit()
        return jsonify(
            {
                "message": "Story rated",
                "data": {oldRating},
            }
        )

@bp.delete("/<int:story_id>/delete")
def delete_story(story_id: int):
    # TODO: Delete rating here, return json. CHECK IF ADMIN!
    return jsonify(
        {
            "message": "Story deleted",
        }
    )


@bp.delete("/<int:story_id>/comment/<int:comment_id>/delete")
def delete_comment(story_id: int, comment_id: int):
    # TODO: Delete comment based on story. CHECK IF ADMIN!
    return jsonify(
        {
            "message": "Comment deleted",
        }
    )
