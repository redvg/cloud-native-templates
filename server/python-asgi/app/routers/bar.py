from fastapi import APIRouter
from models.response import GenericSuccessResponse


router = APIRouter()


@router.get('/zar', response_model=GenericSuccessResponse)
def chat_handler():
    """
    Zar does smth
    """
    return GenericSuccessResponse(detail='ok')
