from typing_extensions import Annotated
import phonenumbers
from pydantic import AfterValidator, BaseModel, EmailStr, StringConstraints


def validate_phonenum(value: str) -> str:
    if len(value) == 0:
        return value
    if value.startswith("0"):
        value = "+62" + value[1:]
    assert phonenumbers.parse(value), f"{value} is not a valid phone number"
    return value


RequiredString = Annotated[str, StringConstraints(min_length=1)]
PhoneNumber = Annotated[str, AfterValidator(validate_phonenum)]


class CreateCommentDTO(BaseModel):
    content: str


class CreateRatingDTO(BaseModel):
    value: int


class UpdateProfileDTO(BaseModel):
    email: EmailStr
    website: str
    phone: PhoneNumber
    about: str
    description: str


class ChangePasswordDTO(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


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
    phone_number: PhoneNumber
    email: EmailStr
