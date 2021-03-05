from sentry_sdk import push_scope
from fastapi import Request, status
from fastapi.responses import JSONResponse
from google.cloud import error_reporting
from google.oauth2 import service_account
from settings.api import api_settings


CONTENT_TYPE_HEADER = 'content-type'
TRACE_ID_HEADER = 'X-Trace-ID'


gcp_credentials = \
    service_account.Credentials.from_service_account_file(api_settings.gcp_pk)

gcp_error_reporting_client = error_reporting.Client(
    project=gcp_credentials.project_id,
    credentials=gcp_credentials,
    service=api_settings.api_name,
    version=api_settings.api_version,
)


def __get_trace_id() -> str:
    trace_id = None
    with push_scope() as scope:
        tx = scope.span
        trace_id = tx.trace_id
    assert trace_id, 'Unexpected trace id: empty'
    return trace_id


def report_exception_to_gcp(req: Request, exc):
    gcp_error_reporting_client.report_exception()
    trace_id = __get_trace_id()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'message': 'Something went wrong..'},
        headers={TRACE_ID_HEADER: trace_id, }
    )


async def add_charset_to_content_type_header(request: Request, call_next):
    response = await call_next(request)
    response_content_type = response.headers.get(CONTENT_TYPE_HEADER, '')
    if response_content_type == 'application/json':
        response.headers[CONTENT_TYPE_HEADER] = \
            'application/json; charset=utf-8'
    return response
