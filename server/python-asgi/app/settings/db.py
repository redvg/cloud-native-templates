from pydantic import BaseSettings


class __DBSettings(BaseSettings):
    collection_users: str = 'users'


db_settings = __DBSettings()
