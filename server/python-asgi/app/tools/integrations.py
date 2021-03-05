from google.oauth2.service_account import \
    Credentials as GCPCredentials
from google.cloud.firestore_v1.async_client import \
    AsyncClient as GCPFirestoreAsyncClient
from google.pubsub_v1.services.publisher.async_client import \
    PublisherAsyncClient as GCPPubSubPublisherAsyncClient
from settings.api import api_settings


credentials: GCPCredentials = \
    GCPCredentials.from_service_account_file(api_settings.gcp_pk)
firestore_client = GCPFirestoreAsyncClient(credentials=credentials)
pubsub_client = GCPPubSubPublisherAsyncClient(credentials=credentials)
