from typing_extensions import Annotated, TypeAlias

from pydantic import BaseModel, StringConstraints, model_validator


class UserDetails(BaseModel):
    pk: int
    username: str
    email: str
    first_name: str
    last_name: str


class PasswordUpdated(BaseModel):
    detail: str


PasswordStr: TypeAlias = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=128,
        strip_whitespace=True,
    ),
]


class PasswordChange(BaseModel):
    new_password: PasswordStr
    confirm_password: PasswordStr

    @model_validator(mode="after")
    def new_password_matches_confirm_password(self) -> "PasswordChange":
        new_password = self.new_password
        confirm_password = self.confirm_password
        if new_password != confirm_password:
            raise ValueError("The new password does not match the confirm one.")
        return self
