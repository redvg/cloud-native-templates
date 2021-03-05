from pydantic import BaseModel


class BaseModelMixin(BaseModel):

    class Config:
        min_anystr_length = 1
        validate_all = True
        allow_mutation = False
        validate_assignment = True
