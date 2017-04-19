from Client import Client
from pathlib import Path
import json, enum


class Pet:
    name = ''
    race = ''
    level = 1
    exp = 0
    needExp = 0
    eatStatus = ''
    playStatus = ''
    bathStatus = ''
    profit = ''
    foodInStock = 0

    def serialize(self):
        pet_dict = {}
        if self.name:
            pet_dict['name'] = self.name
        if self.race:
            pet_dict['race'] = self.race
        if self.level:
            pet_dict['level'] = self.level
        if self.exp:
            pet_dict['exp'] = self.exp
        if self.needExp:
            pet_dict['needExp'] = self.needExp
        if self.eatStatus:
            pet_dict['eatStatus'] = self.eatStatus
        if self.playStatus:
            pet_dict['playStatus'] = self.playStatus
        if self.bathStatus:
            pet_dict['bathStatus'] = self.bathStatus
        if self.profit:
            pet_dict['profit'] = self.profit
        if self.foodInStock:
            pet_dict['foodInStock'] = self.foodInStock
        return pet_dict

    @staticmethod
    def deserialize(pet_dict):
        pet_keys = pet_dict.keys()
        pet = Pet()
        if 'name' in pet_keys:
            pet.name = pet_dict['name']
        if 'race' in pet_keys:
            pet.race = pet_dict['race']
        if 'level' in pet_keys:
            pet.level = pet_dict['level']
        if 'exp' in pet_keys:
            pet.exp = pet_dict['exp']
        if 'needExp' in pet_keys:
            pet.needExp = pet_dict['needExp']
        if 'eatStatus' in pet_keys:
            pet.eatStatus = pet_dict['eatStatus']
        if 'playStatus' in pet_keys:
            pet.playStatus = pet_dict['playStatus']
        if 'bathStatus' in pet_keys:
            pet.bathStatus = pet_dict['bathStatus']
        if 'profit' in pet_keys:
            pet.profit = pet_dict['profit']
        if 'foodInStock' in pet_keys:
            pet.foodInStock = pet_dict['foodInStock']
        return pet


class Configuration:
    autoArena = True
    autoQuest = True
    defaultQuest = 'les'
    autoBattle = True
    autoDonate = False
    donateTill = 0
    autoPet = True
    autoCaptcha = True
    autoCraft = False
    autoEquip = False
    autoTrade = False
    adminUser = None
    orderChat = None
    orderUser = None


class CharacterStatus(enum.Enum):
    UNDEFINED = 0
    REST = 1
    QUEST_LES = 2
    QUEST_CAVE = 3
    QUEST_COW = 4
    ATTACK_BLACK = 5
    ATTACK_RED = 6
    ATTACK_BLUE = 7
    ATTACK_YELLOW = 8
    ATTACK_WHITE = 9
    DEFENCE_BLACK = 10
    DEFENCE_RED = 11
    DEFENCE_BLUE = 12
    DEFENCE_YELLOW = 13
    DEFENCE_WHITE = 14
    ARENA = 15


class Character:
    name = ''
    prof = 0
    pet = None
    stamina = 5
    level = 1
    attack = 1
    defence = 1
    equip = []
    backpack = []
    stockSize = 4000
    stock = []
    exp = 0
    needExp = 0
    arenaWins = 0
    arenaMax = 0
    arenaWalked = 0
    status = CharacterStatus.UNDEFINED

    def __init__(self, client):
        self._client = client
        self._name = client.get_session_name()
        self._config_file = Path(self._name + '.character')
        if self._config_file.is_file():
            self.reload_config_file()
        else:
            self.get_game_info()

    def reload_config_file(self):
        self.deserialize(self._config_file.read_text())

    def get_game_info(self):
        profile = self._client.request_profile()
        stock = self._client.request_stock()
        inv = self._client.request_inv()

    def serialize(self):
        char_dict = {}
        if self.name:
            char_dict['name'] = self.name
        if self.prof:
            char_dict['prof'] = self.prof
        if self.stamina:
            char_dict['stamina'] = self.stamina
        if self.level:
            char_dict['level'] = self.level
        if self.attack:
            char_dict['attack'] = self.attack
        if self.defence:
            char_dict['defence'] = self.defence
        if self.equip:
            char_dict['equip'] = self.equip
        if self.backpack:
            char_dict['backpack'] = self.backpack
        if self.stockSize:
            char_dict['stockSize'] = self.stockSize
        if self.stock:
            char_dict['stock'] = self.stock
        if self.exp:
            char_dict['exp'] = self.exp
        if self.needExp:
            char_dict['needExp'] = self.needExp
        if self.arenaWins:
            char_dict['arenaWins'] = self.arenaWins
        if self.arenaMax:
            char_dict['arenaMax'] = self.arenaMax
        if self.arenaWalked:
            char_dict['arenaWalked'] = self.arenaWalked
        if self.status:
            char_dict['status'] = self.status
        if self.pet:
            char_dict['pet'] = self.pet.serialize()
        return json.dumps(char_dict, ensure_ascii=False)

    def deserialize(self, json_str):
        char_dict = json.loads(json_str)
        keys = char_dict.keys()
        if 'name' in keys:
            self.name = char_dict['name']
        if 'prof' in keys:
            self.prof = char_dict['prof']
        if 'stamina' in keys:
            self.stamina = char_dict['stamina']
        if 'level' in keys:
            self.level = char_dict['level']
        if 'attack' in keys:
            self.attack = char_dict['attack']
        if 'defence' in keys:
            self.defence = char_dict['defence']
        if 'equip' in keys:
            self.equip = char_dict['equip']
        if 'backpack' in keys:
            self.backpack = char_dict['backpack']
        if 'stockSize' in keys:
            self.stockSize = char_dict['stockSize']
        if 'stock' in keys:
            self.stock = char_dict['stock']
        if 'exp' in keys:
            self.exp = char_dict['exp']
        if 'needExp' in keys:
            self.needExp = char_dict['needExp']
        if 'arenaWins' in keys:
            self.arenaWins = char_dict['arenaWins']
        if 'arenaMax' in keys:
            self.arenaMax = char_dict['arenaMax']
        if 'arenaWalked' in keys:
            self.arenaWalked = char_dict['arenaWalked']
        if 'status' in keys:
            self.status = char_dict['status']
        if 'pet' in keys:
            self.pet = Pet.deserialize(char_dict['pet'])

