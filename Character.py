from Client import Client
from pathlib import Path
import json, enum
import time


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
        pet_dict = {'name': self.name, 'race': self.race, 'level': self.level, 'exp': self.exp, 'needExp': self.needExp,
                    'eatStatus': self.eatStatus, 'playStatus': self.playStatus, 'bathStatus': self.bathStatus,
                    'profit': self.profit, 'foodInStock': self.foodInStock}
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
    autoLevelUp = True
    levelUpAtk = True   # Если True, то уровень будет вкачиваться в атаку, если False в защиту.
    adminUser = ''
    orderChat = ''
    orderUser = ''

    def serialize(self):
        conf_dict = {'autoArena': self.autoArena, 'autoQuest': self.autoQuest, 'autoBattle': self.autoBattle,
                     'autoDonate': self.autoDonate, 'donateTill': self.donateTill, 'autoPet': self.autoPet,
                     'autoCaptcha': self.autoCaptcha, 'autoCraft': self.autoCraft, 'autoEquip': self.autoEquip,
                     'autoTrade': self.autoTrade, 'adminUser': self.adminUser, 'orderChat': self.orderChat,
                     'orderUser': self.orderUser, 'autoLevelUp': self.autoLevelUp, 'levelUpAtk': self.levelUpAtk}
        return conf_dict

    @staticmethod
    def deserialize(conf_dict):
        conf_keys = conf_dict.keys()
        conf = Configuration()
        if 'name' in conf_keys:
            conf.name = conf_dict['name']
        if 'race' in conf_keys:
            conf.race = conf_dict['race']
        if 'level' in conf_keys:
            conf.level = conf_dict['level']
        if 'exp' in conf_keys:
            conf.exp = conf_dict['exp']
        if 'needExp' in conf_keys:
            conf.needExp = conf_dict['needExp']
        if 'eatStatus' in conf_keys:
            conf.eatStatus = conf_dict['eatStatus']
        if 'playStatus' in conf_keys:
            conf.playStatus = conf_dict['playStatus']
        if 'bathStatus' in conf_keys:
            conf.bathStatus = conf_dict['bathStatus']
        if 'profit' in conf_keys:
            conf.profit = conf_dict['profit']
        if 'foodInStock' in conf_keys:
            conf.foodInStock = conf_dict['foodInStock']
        if 'autoLevelUp' in conf_keys:
            conf.autoLevelUp = conf_dict['autoLevelUp']
        if 'levelUpAtk' in conf_keys:
            conf.levelUpAtk = conf_dict['levelUpAtk']
        return conf


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


class Castle(enum.Enum):
    UNDEFINED = 0
    BLACK = 1
    RED = 2
    BLUE = 3
    YELLOW = 4
    WHITE = 5


class Timers:
    lastArena = 0.0
    lastQuest = 0.0
    lastProfileRequest = 0.0
    lastBattle = 0.0
    battlesHours = [0, 4, 8, 12, 16, 20]


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
    castle = Castle.UNDEFINED
    alliance = Castle.UNDEFINED
    status = CharacterStatus.UNDEFINED
    config = Configuration()

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
        self._client.request_profile()

    def serialize(self):
        char_dict = {'name': self.name, 'prof': self.prof, 'stamina': self.stamina, 'level': self.level,
                     'attack': self.attack, 'defence': self.defence, 'equip': self.equip, 'backpack': self.backpack,
                     'stockSize': self.stockSize, 'stock': self.stock, 'exp': self.exp, 'needExp': self.needExp,
                     'arenaWins': self.arenaWins, 'arenaMax': self.arenaMax, 'arenaWalked': self.arenaWalked,
                     'status': self.status, 'castle': self.castle, 'alliance': self.alliance,
                     'pet': self.pet.serialize() if self.pet else None, 'config': self.config.serialize()}
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
        if 'castle' in keys:
            self.castle = char_dict['castle']
        if 'alliance' in keys:
            self.alliance = char_dict['alliance']
        if 'pet' in keys:
            self.pet = Pet.deserialize(char_dict['pet'])
        if 'config' in keys:
            self.config = Configuration.deserialize(char_dict['config'])

