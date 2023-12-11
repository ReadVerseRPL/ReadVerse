from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import select
from readverse.plugins import current_user
from readverse.models import Rating, RegularUser, db, Story, Comment
from readverse.dto import CreateCommentDTO, CreateRatingDTO, CreateStoryDTO
from readverse.utils import validate

bp = Blueprint("story", __name__, url_prefix="/story")


@bp.post("/new")
@login_required
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
@login_required
def create_story_page():
    return render_template("pages/story/new.html")


@bp.get("/<int:story_id>")
def read_story(story_id: int):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()
    if not story:
        abort(404, "Story not found!")

    current_rating = None
    if current_user and isinstance(current_user, RegularUser):
        current_rating = db.session.execute(
            select(Rating).where(Rating.author == current_user, Rating.story == story)
        ).scalar_one_or_none()

    return render_template(
        "pages/story/read.html",
        story=story,
        current_rating=current_rating,
    )


@bp.get("/<int:story_id>/edit")
@login_required
def edit_story_page(story_id: int):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        abort(404, "Story not found!")

    if story.author != current_user:
        abort(403, "You are not the owner of that story!")

    return render_template("pages/story/edit.html", story=story)


@bp.post("/<int:story_id>/edit")
@login_required
@validate
def edit_story(story_id: int, form: CreateStoryDTO):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        abort(404, "Story not found!")

    if story.author != current_user:
        abort(403, "You are not the owner of that story!")

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
    comments = db.session.query(Comment).where(Comment.story_id == story_id).all()

    data = [
        {
            "id": comment.id,
            "content": comment.content,
            "timestamp": comment.timestamp.isoformat(),
            "username": comment.author.username,
        }
        for comment in comments
    ]

    return jsonify(
        {
            "message": "Success",
            "data": data,
        }
    )


@bp.post("/<int:story_id>/comment")
@login_required
@validate
def create_comment(story_id: int, json: CreateCommentDTO):
    content = json.content

    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        return jsonify({"message": "Story not found"}), 404

    comment = Comment(content=content, author=current_user, story=story)

    db.session.add(comment)
    db.session.commit()

    return jsonify(
        {
            "message": "Comment created",
            "data": {
                "id": comment.id,
                "content": comment.content,
                "timestamp": comment.timestamp.isoformat(),
                "username": comment.author.username,
            },
        }
    )


@bp.post("/<int:story_id>/rate")
@login_required
@validate
def create_rating(story_id: int, json: CreateRatingDTO):
    value = json.value

    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()

    if not story:
        return jsonify({"message": "Story not found"}), 404

    if story.author == current_user:
        return jsonify({"message": "Cannot rate your own story"}), 403

    old_rating = db.session.execute(
        select(Rating).where(Rating.author == current_user, Rating.story == story)
    ).scalar_one_or_none()

    if not old_rating:
        rating = Rating(
            value=value,
            author=current_user,
            story=story,
        )

        db.session.add(rating)
        db.session.commit()

        return jsonify(
            {
                "message": "Story rated",
                "data": {
                    "value": rating.value,
                    "author_id": rating.author_id,
                    "story_id": rating.story_id,
                },
            }
        )
    else:
        old_rating.value = value
        db.session.commit()
        return jsonify(
            {
                "message": "Story rated",
                "data": {
                    "value": old_rating.value,
                    "author_id": old_rating.author_id,
                    "story_id": old_rating.story_id,
                },
            }
        )


@bp.delete("/<int:story_id>/delete")
@login_required
def delete_story(story_id: int):
    story = db.session.execute(
        select(Story).where(Story.id == story_id)
    ).scalar_one_or_none()
    if not story:
        return jsonify({"message": "Story not found"}), 404

    if story.author_id == current_user.get_id() or current_user.is_admin:
        db.session.delete(story)
        db.session.commit()
        return jsonify(
            {
                "message": "Story deleted",
            }
        )

    return jsonify({"message": "Forbidden"}), 403


@bp.delete("/<int:story_id>/comment/<int:comment_id>/delete")
@login_required
def delete_comment(story_id: int, comment_id: int):
    comment = db.session.execute(
        select(Comment).where(Comment.id == comment_id)
    ).scalar_one_or_none()
    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    if not current_user.is_admin and comment.author != current_user:
        return jsonify({"message": "Forbidden"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify(
        {
            "message": "Comment deleted",
        }
    )
