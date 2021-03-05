from fastapi import Header, status, HTTPException
from hmac import compare_digest
from settings.api import api_settings


class APISecurityInterceptor(object):
    _HEADER_VERSION_INFO: str = 'Target API Version'
    _HEADER_KEY_INFO: str = 'API key'

    @classmethod
    def verify_version(
        cls,
        x_api_version: str = Header(..., description=_HEADER_VERSION_INFO)
    ):
        if x_api_version != api_settings.api_version:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=cls._HEADER_VERSION_INFO,
            )

    @classmethod
    def verify_key(
        cls,
        x_api_key: str = Header(..., description=_HEADER_KEY_INFO),
    ):
        if not compare_digest(x_api_key, api_settings.api_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=cls._HEADER_KEY_INFO,
            )
