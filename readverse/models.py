from datetime import datetime
from typing import TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ARRAY, JSON, Boolean, ForeignKey, MetaData
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, with_polymorphic


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)

if TYPE_CHECKING:
    BaseModel = Base
else:
    BaseModel = db.Model


class User(BaseModel):
    __tablename__ = "user"
    is_admin = False

    # Flask-Login stuffs
    is_authenticated = True
    is_active = True
    is_anonymous = False

    username: Mapped[str] = mapped_column(String, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    def get_id(self):
        return self.username

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }


class Admin(User):
    __tablename__ = "admin"
    username: Mapped[str] = mapped_column(ForeignKey("user.username"), primary_key=True)

    is_admin = True

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class RegularUser(User):
    __tablename__ = "regularuser"
    username: Mapped[str] = mapped_column(ForeignKey("user.username"), primary_key=True)
    about: Mapped[str] = mapped_column(String)
    website: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    stories: Mapped[list["Story"]] = relationship(back_populates="author")

    __mapper_args__ = {
        "polymorphic_identity": "regular",
    }


class Story(BaseModel):
    __tablename__ = "story"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    genres: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    author_id: Mapped[str] = mapped_column(ForeignKey("user.username"))
    author: Mapped[RegularUser] = relationship(back_populates="stories")

    comments: Mapped[list["Comment"]] = relationship(back_populates="story")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="story")


class Comment(BaseModel):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    author_id: Mapped[str] = mapped_column(ForeignKey("user.username"))
    author: Mapped[RegularUser] = relationship(RegularUser)

    story_id: Mapped[int] = mapped_column(ForeignKey("story.id"))
    story: Mapped[Story] = relationship(Story, back_populates="comments")


class Rating(BaseModel):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)

    author_id: Mapped[str] = mapped_column(ForeignKey("user.username"))
    author: Mapped[RegularUser] = relationship(RegularUser)

    story_id: Mapped[int] = mapped_column(ForeignKey("story.id"))
    story: Mapped[Story] = relationship(Story, back_populates="ratings")


AllUser = with_polymorphic(User, [Admin, RegularUser])
