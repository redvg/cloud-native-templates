from pydantic import BaseModel, Field
from typing import Optional


class FooRequest(BaseModel):
    foo: Optional[str] = Field(
        None,
        description='foo',
        example='foo',
        min_length=1,
        regex='^[a-zA-Z0-9]+$',
    )


class FooResponse(BaseModel):
    foo: str = Field(
        ...,
        description='foo',
        example='foo',
        min_length=1,
        regex='^[a-zA-Z0-9]+$',
    )
