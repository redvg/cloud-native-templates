from pydantic import BaseSettings


class __APISettings(BaseSettings):
    api_version: str = 'v1'
    api_name: str = 'api'
    url_api_sandbox: str = '/sandbox'
    url_api_docs: str = '/docs'
    url_protected: str = '/protected'
    url_public: str = '/public'
    api_key: str
    is_staging: bool
    gcp_pk: str
    gcp_project_id: str
    jwt_iss: str
    sentry_dsn: str
    sentry_trace_sampling_rate: float

    class Config:
        env_file = '.env'


api_settings = __APISettings()
