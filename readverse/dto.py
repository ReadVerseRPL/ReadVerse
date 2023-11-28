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
