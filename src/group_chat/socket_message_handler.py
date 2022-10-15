import json

from broadcaster import Broadcast

from data.schemas.users.user import User
from group_chat.group_chat_message_data import GroupChatMessageData

async def handle_message(channel: str, message_data: dict, current_user: User, broadcast: Broadcast):
    text = GroupChatMessageData(**message_data)
    payload_dict = {"user": current_user.email, "text": text.text}
    payload_str = json.dumps(payload_dict)
    await broadcast.publish(channel, payload_str)
