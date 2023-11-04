from base import *
from typing import Union


class ActionType(JsonIntEnum):
    """Action space."""
    SILENT = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    PLACED = 5


class InitReq(JsonBase):
    """Init request payload."""
    def __init__(self, player_name:str) -> None:
        super().__init__()
        self.player_name = player_name


class ActionReq(JsonBase):
    """Action request payload."""

    def __init__(
        self, playerID: int, actionType: ActionType) -> None:
        super().__init__()
        self.playerID = playerID
        self.actionType = actionType


class PacketReq(JsonBase):
    """The basic packet of communication with the server."""

    def __init__(
        self, type: PacketType, data: Union[InitReq, ActionReq]
    ) -> None:
        super().__init__()
        self.type = type
        self.data = data