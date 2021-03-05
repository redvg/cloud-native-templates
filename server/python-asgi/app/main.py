from typing import Any, Union
import uvicorn
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi import Depends, FastAPI, status
from settings.api import api_settings
from models.response import GenericErrorResponse
from tools.api import APISecurityInterceptor
from tools.auth import jwt_bearer
from tools.middleware import \
    report_exception_to_gcp,\
    add_charset_to_content_type_header
from routers.foo import router as foo_router
from routers.bar import router as bar_router


responses: dict[Union[int, str], dict[str, Any]] = {
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Bad request, check body',
        'model': GenericErrorResponse,
    },
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Unauthorized, check headers',
        'model': GenericErrorResponse,
    },
    status.HTTP_403_FORBIDDEN: {
        'description': 'Forbidden, check headers',
        'model': GenericErrorResponse,
    },
    status.HTTP_429_TOO_MANY_REQUESTS: {
        'description': 'Too many requests, retry later',
        'model': GenericErrorResponse,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        'description': 'Server failed',
    },
}


app = FastAPI(
    title='Some API',
    version=api_settings.api_version,
    docs_url=api_settings.url_api_sandbox if api_settings.is_staging else None,
    redoc_url=api_settings.url_api_docs if api_settings.is_staging else None,
    openapi_url='/openapi.json' if api_settings.is_staging else None,
)

app.add_exception_handler(500, report_exception_to_gcp)

app.middleware('http')(add_charset_to_content_type_header)

app.include_router(
    foo_router,
    prefix=api_settings.url_protected,
    tags=['Protected'],
    responses=responses,
    dependencies=[
        Depends(APISecurityInterceptor.verify_key),
        Depends(APISecurityInterceptor.verify_version),
        Depends(jwt_bearer),
    ],
)

app.include_router(
    bar_router,
    prefix=api_settings.url_public,
    tags=['Public'],
    responses=responses,
)

sentry_sdk.init(
    dsn=api_settings.sentry_dsn,
    traces_sample_rate=api_settings.sentry_trace_sampling_rate,
    send_default_pii=api_settings.is_staging,
    environment='staging' if api_settings.is_staging else 'production'
)

asgi_app = SentryAsgiMiddleware(app)


if __name__ == '__main__':
    uvicorn.run(asgi_app, host='0.0.0.0', port=8000)
