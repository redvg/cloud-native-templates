from __future__ import annotations

from pydantic import BaseModel, validator
from models.mixin import BaseModelMixin


class AuthorisedUser(BaseModel):
    auth_id: str

    @classmethod  # type: ignore
    @validator('auth_id')
    def auth_id_must_have_expected_length(cls, v):
        if len(v) < 1:
            raise ValueError('Unexpected user id: empty')
        return v


class User(BaseModelMixin, BaseModel):
    id: str
    name: str

    @staticmethod
    def from_doc(doc: dict) -> User:
        user: User = User(
            id=doc['id'],
            name=doc['id'],
        )
        return user
