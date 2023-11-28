from flask import Blueprint, jsonify, redirect, render_template, request, url_for

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
def edit_story_page():
    return render_template("pages/story/edit.html")


@bp.post("/<int:story_id>/edit")
@validate
def edit_story(form: CreateStoryDTO):
    # TODO: Edit story based on input and redirect to story
    return redirect(url_for("story.read_story", story_id=-1))


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
