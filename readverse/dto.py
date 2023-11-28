from pydantic import BaseModel


class CreateCommentDTO(BaseModel):
    content: str


class CreateRatingDTO(BaseModel):
    value: int


class CreateStoryDTO(BaseModel):
    title: str
    description: str
    content: str
    genres: list[str]


class SearchQueryDTO(BaseModel):
    query: int | None = None


class LoginFormDTO(BaseModel):
    username: str
    password: str


class RegisterFormDTO(LoginFormDTO):
    phone_number: str
    email: str
