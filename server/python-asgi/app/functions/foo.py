from google.pubsub_v1.types.pubsub import PubsubMessage
from settings.api import api_settings
from tools.integrations import pubsub_client


async def publish_to_mq(
    id: str,
    name: str,
) -> None:
    topic: str = pubsub_client.topic_path(
        api_settings.gcp_project_id,
        'topic'
    )
    message_data = u'msg'
    encoded_message_data: bytes = message_data.encode('utf-8')
    message_attributes: dict[str, str] = {
        'id': id,
        'name': name,
    }
    message: PubsubMessage = PubsubMessage(
        data=encoded_message_data,
        attributes=message_attributes,
    )
    await pubsub_client.publish(
        topic=topic,
        messages=[message],
    )
    return
