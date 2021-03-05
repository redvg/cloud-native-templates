from typing import Union, AsyncIterator, cast
from google.cloud.firestore_v1.async_client import AsyncClient
from google.cloud.firestore_v1.async_collection import AsyncCollectionReference
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from tools.integrations import firestore_client
from settings.db import db_settings
from models.user import User


class __DbManager(object):
    def __init__(self):
        self.client: AsyncClient = firestore_client
        self.users: AsyncCollectionReference = \
            self.client.collection(
                db_settings.firestore_collection_users,  # type: ignore
            )

    async def get_user_by_auth_id(self, auth_id: str) -> User:
        user: Union[User, None] = None
        docs: AsyncIterator[DocumentSnapshot] = self.users\
            .where('authId', '==', auth_id)\
            .stream()  # type: ignore
        async for each in docs:
            parsed_doc: dict = cast(dict, each.to_dict())
            user = User.from_doc(doc=parsed_doc)
            break
        assert user, 'Cannot find user'
        return user


db_manager = __DbManager()
