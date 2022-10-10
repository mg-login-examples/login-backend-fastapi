from broadcaster import Broadcast

from data.schemas.users.user import User
from group_chat.group_chat_message_data import GroupChatMessageData

async def handle_message(channel: str, message_data: dict, current_user: User, broadcast: Broadcast):
    text = GroupChatMessageData(**message_data)
    await broadcast.publish(channel, {"user": current_user.email, "text": text.text})
