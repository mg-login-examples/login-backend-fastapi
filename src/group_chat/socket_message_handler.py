import json

from data.schemas.users.user import User
from group_chat.group_chat_message_data import GroupChatMessageData
from utils.pubsub.pubsub import PubSub


async def handle_message(
    channel: str, message_data: dict, current_user: User, pubsub: PubSub
):
    text = GroupChatMessageData(**message_data)
    payload_dict = {"user": current_user.email, "text": text.text}
    payload_str = json.dumps(payload_dict)
    await pubsub.publish(channel, payload_str)
