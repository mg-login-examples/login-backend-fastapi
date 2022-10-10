from enum import Enum

class WebSocketActions(Enum):
    MESSAGE = "message"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
