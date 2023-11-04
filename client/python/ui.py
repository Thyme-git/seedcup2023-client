from base import *
from resp import *
from enum import Enum
from random import choice as random_choice
from config import config

class Emoji(Enum):
    """Kawaii emojis!"""
    # Bricks
    HoneyBrick = "🍯"
    BottleBrick = "🏺"
    SunFlowerBrick = "🌻"
    RedBrick = "🟥"
    GreenBrick = "🟩"
    BlueBrick = "🟦"
    BlackBrick = "⬛"
    ObstacleBrick = "🧱"
    BombedBrick =  "💥"
    NullBlrick = "◻️ "
    
    # players
    Character1 = "🦸‍️"
    Character2 = "🦹‍️️"
    Character3 = "🧝️"
    Character4 = "🧛"
    CharacterInvencible = "👼"
    CharacterShield = "👒"

    # Items
    Hp = "💖"
    Speed = "🛼"
    Bomb = "💣"
    BombNum = "💊"
    Shield = "🔰"
    BombRange = "🧪"
    Invencible = "🗽"

    @property
    def emoji(self):
        return self._value_


removableBlock = [Emoji.HoneyBrick,
                  Emoji.BottleBrick,
                  Emoji.SunFlowerBrick,
                  Emoji.RedBrick,
                  Emoji.GreenBrick,
                  Emoji.BlueBrick]


CharacterUsed = [Emoji.Character1,
                 Emoji.Character2,
                 Emoji.Character3,
                 Emoji.Character4]


playerID2Emoji = {0:Emoji.Character1.emoji,
                  1:Emoji.Character2.emoji,} # to be allocated


itemType2Emoji = {
    ItemType.HP: Emoji.Hp.emoji,
    ItemType.BOMB_RANGE: Emoji.BombRange.emoji,
    ItemType.BOMB_NUM: Emoji.BombNum.emoji,
    ItemType.INVINCIBLE: Emoji.Invencible.emoji,
    ItemType.SHIELD: Emoji.Shield.emoji
}

class Block(object):
    def __init__(
        self,
    ) -> None:
        self._removable = False
        self._emoji = None
    
    def refresh(self, obj:Obj, last_bomb = False) -> None:
        if last_bomb:
            self._emoji = Emoji.BombedBrick.emoji
        
        elif obj is None or obj.type == ObjType.Null:
            self._removable = False
            self._emoji = Emoji.NullBlrick.emoji
        
        elif obj.type == ObjType.Player:
            if obj.property.invincible_time > 0:
                self._emoji = Emoji.CharacterInvencible.emoji
            elif obj.property.shield_time > 0:
                self._emoji = Emoji.CharacterShield.emoji
            else:
                self._emoji = playerID2Emoji[obj.property.player_id]

        elif obj.type== ObjType.Bomb:
            self._emoji = Emoji.Bomb.emoji
        
        elif obj.type == ObjType.Block:
            if obj.property.removable and self._removable == False:
                self._removable = True
                self._emoji = random_choice(removableBlock).emoji
            elif not obj.property.removable:
                self._removable = False
                self._emoji = Emoji.ObstacleBrick.emoji
        
        elif obj.type == ObjType.Item:
            self._emoji = itemType2Emoji[obj.property.item_type]

    @property
    def emoji(self):
        return self._emoji

class UI(object):
    def __init__(
        self,
        player_id: int = -1,
    ) -> None:
        range_x = config.get("map_size")
        range_y = config.get("map_size")
        self._player_id = player_id
        self._player: Player = None
        self._block = [[Block() for _ in range(range_x)] for __ in range(range_y)]

    def display(self) -> None:
        if self._player is not None:
            print(
                f"playerID: {self._player.player_id}, "\
                f"Charactor: {playerID2Emoji[self._player.player_id]}, "\
                f"{Emoji.Hp.emoji}:{self._player.hp}, "\
                f"{Emoji.Invencible.emoji}: {self._player.invincible_time}, "\
                f"{Emoji.Shield.emoji}: {self._player.shield_time}, "\
                f"{Emoji.BombRange.emoji}: {self._player.bomb_range}, "\
                f"{Emoji.BombNum.emoji}: {self._player.bomb_max_num}, "\
                f"{Emoji.Bomb.emoji}: {self._player.bomb_now_num}, "\
                f"Score: {self._player.score}"
            )

        for block_row in self._block:
            for block in block_row:
                print(block.emoji, end='')
            print('')

    def refresh(self, actionResp: ActionResp) -> None:
        for map in actionResp.map:
            freshed = False
            if len(map.objs):
                for obj in map.objs:
                    if obj.type == ObjType.Player and obj.property.alive:
                        if obj.property.player_id not in playerID2Emoji.keys():
                            _emoji = random_choice(CharacterUsed)
                            CharacterUsed.remove(_emoji)
                            playerID2Emoji[obj.property.player_id] = _emoji.emoji
                        if obj.property.player_id == self._player_id:
                            self._player = obj.property
                        
                        self._block[map.x][map.y].refresh(obj)
                        freshed = True
                        break
                
                if not freshed:
                    self._block[map.x][map.y].refresh(map.objs[0])

            else:
                self._block[map.x][map.y].refresh(None, actionResp.round == map.last_bomb_round)

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, value):
        self._player_id = value