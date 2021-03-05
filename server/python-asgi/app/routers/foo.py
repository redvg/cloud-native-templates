from fastapi import APIRouter, Depends
from models.foo import FooRequest, FooResponse
from models.user import AuthorisedUser, User
from tools.auth import jwt_bearer
from tools.db import db_manager
from functions.foo import publish_to_mq


router = APIRouter()


@router.post('', response_model=FooResponse)
async def chat_handler(
    req: FooRequest,
    auth_user: AuthorisedUser = Depends(jwt_bearer),
):
    """
    Foo does smth
    """
    user: User = await \
        db_manager.get_user_by_auth_id(auth_id=auth_user.auth_id)
    await publish_to_mq(
        id=req.foo,
        name=user.name,
    )
    return FooResponse(foo='ok')
