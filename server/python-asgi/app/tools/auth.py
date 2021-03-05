import firebase_admin
from firebase_admin import auth, credentials
from fastapi import status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from typing import Optional, Dict, Any, Tuple, Union
from models.user import AuthorisedUser
from settings.api import api_settings


class JWTException(Exception):
    def __init__(self, message, code=None, cause=None, http_response=None):
        Exception.__init__(self, message)
        self._code = code
        self._cause = cause
        self._http_response = http_response

    @property
    def code(self):
        return self._code

    @property
    def cause(self):
        return self._cause

    @property
    def http_response(self):
        return self._http_response


class MissingUserClaimsError(JWTException):
    """
    JWT does not contain expected user claims: might be compromised
    """
    def __init__(self):
        JWTException.__init__(self, 'Invalid token: user claims missing')


class UnexpectedClientClaimsError(JWTException):
    """
    JWT was issued to unknown client: scoping issue or compromised
    """
    def __init__(self):
        JWTException.__init__(self, 'Invalid token: unexpected client')


class UnexpectedIssuerOrAudienceClaimsError(JWTException):
    """
    JWT has unexpected issuer or audience: might be compromised
    """
    def __init__(self):
        JWTException.__init__(self, 'Invalid token: not well known')


class UnverifiedEmailClaimsError(JWTException):
    """
    JWT reports unverified user email: user should not be allowed to proceed
    """
    def __init__(self):
        JWTException.__init__(self, 'Invalid token: not well known')


class __JWTBearer(HTTPBearer):
    _NAME: str = 'Authorization: Bearer JWT'
    _UNAUTHORIZED_STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DEFAULT_UNAUTHORIZED_EXCEPTION = HTTPException(
        status_code=_UNAUTHORIZED_STATUS_CODE,
        detail='Invalid bearer',
        headers={'WWW-Authenticate': 'Bearer type=jwt realm=foo'}
    )
    _WELL_KNOWN_AUD: str = api_settings.gcp_project_id
    _WELL_KNOWN_ISS: str = api_settings.jwt_iss + '/' + _WELL_KNOWN_AUD

    def __init__(self, gapi_auth_client, auto_error: bool = False):
        super().__init__(auto_error=auto_error, scheme_name=self._NAME)
        assert gapi_auth_client, 'Invalid GAPI auth client'
        self.gapi_auth_client = gapi_auth_client

    def __validate_and_parse_jwt_claims(
        self,
        claims: Dict[str, Any]
    ) -> AuthorisedUser:
        aud: str = claims.get('aud', '')
        if not aud or aud != self._WELL_KNOWN_AUD:
            raise UnexpectedIssuerOrAudienceClaimsError
        iss: str = claims.get('iss', '')
        if not iss or iss != self._WELL_KNOWN_ISS:
            raise UnexpectedIssuerOrAudienceClaimsError
        is_email_verified: bool = claims.get('email_verified', False)
        if not is_email_verified:
            raise UnverifiedEmailClaimsError
        user_id: str = claims.get('user_id', '')
        if not user_id:
            raise MissingUserClaimsError
        user = AuthorisedUser(auth_id=user_id)
        return user

    async def __verify_jwt(
        self,
        jwt: str,
    ) -> Tuple[bool, str, Union[AuthorisedUser, None]]:
        try:
            claims: dict = auth.verify_id_token(
                jwt,
                check_revoked=True,
                app=self.gapi_auth_client
            )
            user: AuthorisedUser = \
                self.__validate_and_parse_jwt_claims(claims=claims)
            return True, 'ok', user
        except auth.RevokedIdTokenError:
            return False, 'Token revoked', None
        except firebase_admin._token_gen.ExpiredIdTokenError:  # type: ignore
            return False, 'Token expired', None
        except auth.InvalidIdTokenError:
            return False, 'Invalid token', None
        except JWTException as e:
            return False, str(e), None

    async def __call__(self, request: Request) -> Optional[AuthorisedUser]:
        authz_credentials: HTTPAuthorizationCredentials = \
            await super().__call__(request)  # type: ignore
        if not authz_credentials:
            raise self._DEFAULT_UNAUTHORIZED_EXCEPTION
        if not authz_credentials.scheme == "Bearer":
            raise self._DEFAULT_UNAUTHORIZED_EXCEPTION
        if not authz_credentials.credentials:
            raise self._DEFAULT_UNAUTHORIZED_EXCEPTION
        jwt: str = authz_credentials.credentials
        is_ok, msg, user = await self.__verify_jwt(jwt=jwt)
        if not is_ok:
            assert msg, 'Expecting unauthZ\'d message'
            raise HTTPException(
                status_code=self._UNAUTHORIZED_STATUS_CODE,
                detail=msg,
            )
        else:
            assert user, 'Expecting user'
            return user


_client_cert = credentials.Certificate(api_settings.gcp_pk)
_firebase_auth_client = firebase_admin.initialize_app(_client_cert)
jwt_bearer = __JWTBearer(gapi_auth_client=_firebase_auth_client)
