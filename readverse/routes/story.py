from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from sqlalchemy import select
from readverse.plugins import current_user
from readverse.models import db, Story
from readverse.dto import CreateCommentDTO, CreateRatingDTO, CreateStoryDTO
from readverse.utils import validate

bp = Blueprint("story", __name__, url_prefix="/story")


@bp.post("/new")
@validate
def create_story(form: CreateStoryDTO):
    # TODO: Create story based on input and redirect to story
    return redirect(url_for("story.read_story", story_id=-1))


@bp.get("/new")
def create_story_page():
    return render_template("pages/story/new.html")


@bp.get("/<int:story_id>")
def read_story(story_id: int):
    # TODO: Get story by ID
    return render_template("pages/story/read.html")


@bp.get("/<int:story_id>/edit")
def edit_story_page(story_id: int):
    return render_template("pages/story/edit.html")


@bp.post("/<int:story_id>/edit")
@validate
def edit_story(story_id: int, form: CreateStoryDTO):
    # TODO [DONE]: Edit story based on input and redirect to story
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        abort(404)

    # Check and handle 'genres' field if it's a string
    genres = form.genres
    if isinstance(genres, str):
        genres = [genres]

    # Update the story's attributes
    story.title = form.title
    story.description = form.description
    story.content = form.content
    story.genres = genres

    # Save the updated story back to the database
    db.session.commit()

    # Redirect to the updated story's page
    return redirect(url_for("story.read_story", story_id=story.id))


@bp.get("/<int:story_id>/comments")
def comments(story_id: int):
    # TODO: Get all comments and return as json
    return jsonify([])


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
    # TODO: Create rating object based on json data and save, then return json
    value = json.value

    return jsonify(
        {
            "message": "Story rated",
            "data": {},  # TODO: Rating data here
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
