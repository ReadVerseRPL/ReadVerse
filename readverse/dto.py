from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints

RequiredString = Annotated[str, StringConstraints(min_length=1)]


class CreateCommentDTO(BaseModel):
    content: str


class CreateRatingDTO(BaseModel):
    value: int


class CreateStoryDTO(BaseModel):
    title: RequiredString
    description: RequiredString
    content: RequiredString
    genres: list[RequiredString] | RequiredString = []


class SearchQueryDTO(BaseModel):
    query: str | None = None


class LoginFormDTO(BaseModel):
    username: str
    password: str


class RegisterFormDTO(LoginFormDTO):
    phone_number: str
    email: str
