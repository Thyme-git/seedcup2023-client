from base import *
from typing import Union, List


class ItemType(JsonIntEnum):
    NO_POTION = 0
    BOMB_RANGE = 1
    BOMB_NUM = 2
    HP = 3
    INVINCIBLE = 4
    SHIELD = 5


class ObjType(JsonIntEnum):
    Null = 0
    Player = 1
    Bomb = 2
    Block = 3
    Item = 4


class Player(JsonBase):
    def __init__(
        self,
        player_id: int = 0,
        alive: bool = True,
        hp: int = 0,
        shield_time: int = 0,
        invincible_time: int = 0,  
        score: int = 0,           
        bomb_range: int = 1,       
        bomb_max_num: int = 1,     
        bomb_now_num: int = 1,
        speed: int = 0,  
    ) -> None:
        super().__init__()
        self.player_id = player_id
        self.alive = alive
        self.hp = hp
        self.shield_time = shield_time
        self.invincible_time = invincible_time
        self.score = score
        self.bomb_range = bomb_range
        self.bomb_max_num = bomb_max_num
        self.bomb_now_num = bomb_now_num
        self.speed = speed


class Bomb(JsonBase):
    def __init__(
        self,
        bomb_id: int = 0,
        bomb_range: int = 1,
        player_id: int = 0
    ) -> None:
        super().__init__()
        self.bomb_id = bomb_id
        self.bomb_range = bomb_range
        self.player_id = player_id


class Block(JsonBase):
    def __init__(
        self,
        block_id: int = 0,
        removable: bool = False
    ) -> None:
        super().__init__()
        self.block_id = block_id
        self.removable = removable


class Item(JsonBase):
    def __init__(
        self,
        item_type: ItemType = ItemType.NO_POTION
    ) -> None:
        super().__init__()
        self.item_type = item_type


class Obj(JsonBase):
    def __init__(
        self,
        type: ObjType = ObjType.Null,
        property: Union[None, Player, Bomb, Block, Item] = None,
    ) -> None:
        super().__init__()
        self.type = type
        self.property = property

    def from_json(self, j: str):
        d = json.loads(j)
        self.type = self.type.from_json(d.pop("type"))
        property = d.pop("property")
        if self.type == ObjType.Player:
            self.property = Player().from_json(json.dumps(property))
        
        elif self.type == ObjType.Bomb:
            self.property = Bomb().from_json(json.dumps(property))
        
        elif self.type == ObjType.Block:
            self.property = Block().from_json(json.dumps(property))
        
        elif self.type == ObjType.Item:
            self.property = Item().from_json(json.dumps(property))

        return self


class Map(JsonBase):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        last_bomb_round: int = -1,
        objs: List[Obj] = [],
    ) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.last_bomb_round = last_bomb_round
        self.objs = objs

    def from_json(self, j: str):
        d = json.loads(j)
        for key, value in d.items():
            if key in self.__dict__:
                if key == "objs":
                    self.objs = [Obj().from_json(json.dumps(v)) for v in value]
                elif hasattr(self.__dict__[key], "from_json"):
                    setattr(self, key, self.__dict__[key].from_json(json.dumps(value)))
                else:
                    setattr(self, key, value)
        return self


class ActionResp(JsonBase):
    def __init__(
        self,
        player_id: int = 0,
        round: int = 0,
        map: List[Map] = [],
    ) -> None:
        super().__init__()
        self.player_id = player_id
        self.round = round
        self.map = map

    def from_json(self, j: str):
        d = json.loads(j)
        for key, value in d.items():
            if key in self.__dict__:
                if key == "map":
                    self.map = [Map().from_json(json.dumps(v)) for v in value]
                if hasattr(self.__dict__[key], "from_json"):
                    setattr(self, key, self.__dict__[key].from_json(json.dumps(value)))
                elif key != "map":
                    setattr(self, key, value)
        return self


class GameOverResp(JsonBase):
    def __init__(
        self,
        scores: List = [],
        winner_ids: list = []
    ) -> None:
        super().__init__()
        self.scores = scores
        self.winner_ids = winner_ids
    
    def from_json(self, j: str):
        d = json.loads(j)
        self.scores = d["scores"]
        self.winner_ids = d["winner_ids"]
        return self


class PacketResp(JsonBase):
    def __init__(
        self,
        type: PacketType = PacketType.ActionResp,
        data: Union[ActionResp, GameOverResp] = ActionResp(),
    ) -> None:
        super().__init__()
        self.type = type
        self.data = data

    def from_json(self, j: str):
        d = json.loads(j)
        self.type = self.type.from_json(d.pop("type"))
        data = d.pop("data")
        if self.type == PacketType.ActionResp:
            self.data = ActionResp().from_json(json.dumps(data))
        elif self.type == PacketType.GameOver:
            self.data = GameOverResp().from_json(json.dumps(data))

        return self