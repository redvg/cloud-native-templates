from pydantic import BaseModel


class GenericErrorResponse(BaseModel):
    detail: str = 'string'


class GenericSuccessResponse(BaseModel):
    detail: str = 'string'
