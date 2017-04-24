# -*- coding: utf-8 -*-
from pathlib import Path
import json, enum
import time
import re
import regexp
import pytz
from pytz import timezone
from datetime import datetime, timedelta
from enums import *
from random import randint


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
    defaultQuest = Quest.LES
    autoBattle = True
    autoDonate = False
    donateTill = 0
    autoPet = True
    autoCaptcha = True
    autoCraft = False
    autoEquip = False
    autoTrade = False
    autoLevelUp = True
    # Если levelUpAtk True, то уровень будет вкачиваться в атаку, если False в защиту.
    levelUpAtk = True

    def serialize(self):
        conf_dict = {'autoArena': self.autoArena, 'autoQuest': self.autoQuest, 'autoBattle': self.autoBattle,
                     'autoDonate': self.autoDonate, 'donateTill': self.donateTill, 'autoPet': self.autoPet,
                     'autoCaptcha': self.autoCaptcha, 'autoCraft': self.autoCraft, 'autoEquip': self.autoEquip,
                     'autoTrade': self.autoTrade, 'autoLevelUp': self.autoLevelUp, 'levelUpAtk': self.levelUpAtk}
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


class Timers:
    lastArenaStart = 0.0
    lastArenaEnd = 0.0
    lastQuest = 0.0
    lastProfileUpdate = 0.0
    lastStockUpdate = 0.0
    lastEquipUpdate = 0.0

    def serialize(self):
        time_dict = {'lastArenaStart': self.lastArenaStart, 'lastQuest': self.lastQuest,
                     'lastProfileUpdate': self.lastProfileUpdate, 'lastArenaEnd': self.lastArenaEnd,
                     'lastStockUpdate': self.lastStockUpdate, 'lastEquipUpdate': self.lastEquipUpdate}
        return time_dict

    @staticmethod
    def deserialize(timers_dict):
        timers = Timers()
        keys = timers_dict.keys()
        if 'lastArenaStart' in keys:
            timers.lastArenaStart = timers_dict['lastArenaStart']
        if 'lastArenaEnd' in keys:
            timers.lastArenaEnd = timers_dict['lastArenaEnd']
        if 'lastQuest' in keys:
            timers.lastQuest = timers_dict['lastQuest']
        if 'lastProfileUpdate' in keys:
            timers.lastProfileUpdate = timers_dict['lastProfileUpdate']
        if 'lastStockUpdate' in keys:
            timers.lastStockUpdate = timers_dict['lastStockUpdate']
        if 'lastEquipUpdate' in keys:
            timers.lastEquipUpdate = timers_dict['lastEquipUpdate']
        return timers


class Character:
    name = ''
    prof = ''
    pet = None
    stamina = 5
    maxStamina = 5
    level = 1
    attack = 1
    defence = 1
    equip = None
    backpack = None
    stockSize = 4000
    stock = None
    exp = 0
    needExp = 0
    arenaWins = 0
    arenaMax = 0
    arenaWalked = 0
    castle = Castle.UNDEFINED
    alliance = Castle.UNDEFINED
    status = CharacterStatus.UNDEFINED
    config = Configuration()
    timers = Timers()
    gold = 0
    donateGold = 0

    _needProfileRequest = False
    _needHeroRequest = False
    _needPetRequest = False
    _needStockRequest = False
    _needInvRequest = False
    _needLevelUp = False
    _currentOrder = Castle.UNDEFINED

    def __init__(self, client):
        # self._client = client
        self._name = client
        self._config_file = Path(self._name + '.character')
        if self._config_file.is_file():
            self.reload_config_file()
        else:
            self._needProfileRequest = True

    def reload_config_file(self):
        self.deserialize(self._config_file.read_text('utf8'))

    def save_config_file(self):
        config = self.serialize()
        self._config_file.write_text(config, 'utf8')

    def ask_action(self):
        if self.status == CharacterStatus([CharacterAction.ATTACK, self._currentOrder]) and datetime.now().time().hour in [0, 4, 8, 12, 16, 20]:
            self.status = CharacterStatus.REST
        if self.status == CharacterStatus.QUEST_LES and self.timers.lastQuest + 300 < time.time():
            self.status = CharacterStatus.REST
        if self.status == CharacterStatus.REST:
            if self.status != CharacterStatus([CharacterAction.ATTACK, self._currentOrder]) and \
                            datetime.now().time().hour in [23, 3, 7, 11, 15, 19] and datetime.now().time().minute > 40:
                self.status = CharacterStatus([CharacterAction.ATTACK, self._currentOrder])
                return self.status.value
            elif self.timers.lastProfileUpdate + 3600 < time.time():
                self.status = CharacterStatus.WAITING_DATA
                return [CharacterAction.GET_DATA]
            elif self.stamina > 0 and self.config.defaultQuest == Quest.LES:
                self.timers.lastQuest = time.time() + randint(10, 180)
                self.status = CharacterStatus.QUEST_LES
                self.stamina -= 1
                self.save_config_file()
                return [CharacterAction.QUEST, self.config.defaultQuest]
        return [CharacterAction.WAIT]

    def set_order(self, order):
        try:
            self._currentOrder = Castle(order)
            if self.status != CharacterStatus([CharacterAction.ATTACK, self._currentOrder]) or \
                            self.status != CharacterStatus([CharacterAction.DEFENCE, self._currentOrder]):
                self.status = CharacterStatus.REST
        except ValueError:
            pass

    def parse_profile(self, profile):
        parsed_data = re.search(regexp.main_hero, profile)
        if parsed_data.group(1):
            self._needLevelUp = True
        self.castle = Castle(str(parsed_data.group(4)))
        self.name = str(parsed_data.group(5))
        self.prof = str(parsed_data.group(6))
        self.level = int(parsed_data.group(7))
        self.attack = int(parsed_data.group(8))
        self.defence = int(parsed_data.group(9))
        self.exp = int(parsed_data.group(10))
        self.needExp = int(parsed_data.group(11))
        self.stamina = int(parsed_data.group(12))
        self.maxStamina = int(parsed_data.group(13))
        self.gold = int(parsed_data.group(14))
        self.donateGold = int(parsed_data.group(15))
        if not self.stock:
            self._needStockRequest = True
        if (not self.equip or not self.backpack) \
                and str(parsed_data.group(16)) != '[-]'\
                and int(parsed_data.group(17)) != 0:
            self._needInvRequest = True
        if parsed_data.group(19) and not self.pet or str(parsed_data.group(20)) != '😁':
            self._needPetRequest = True
        self.status = self._parse_status(parsed_data.group(23))
        self.timers.lastProfileUpdate = time.time() + randint(50, 3600)
        self.save_config_file()

    def _parse_status(self, status):
        if StatusText.REST.value in status:
            return CharacterStatus.REST
        elif StatusText.LES.value in status:
            return CharacterStatus.QUEST_LES
        elif StatusText.CAVE.value in status:
            return CharacterStatus.QUEST_CAVE
        elif StatusText.COW.value in status:
            return CharacterStatus.QUEST_COW
        elif StatusText.ARENA.value in status:
            return CharacterStatus.ARENA
        elif StatusText.ATTACK.value in status:
            castle = self._find_castle(status)
            return CharacterStatus([CharacterAction.ATTACK, castle])
        elif StatusText.DEFENCE.value in status:
            castle = self._find_castle(status)
            return CharacterStatus([CharacterAction.DEFENCE, castle])
        return CharacterStatus.UNDEFINED

    def _find_castle(self, somestr):
        if Castle.BLACK.value in somestr:
            return Castle.BLACK
        elif Castle.BLUE.value in somestr:
            return Castle.BLUE
        elif Castle.RED.value in somestr:
            return Castle.RED
        elif Castle.WHITE.value in somestr:
            return Castle.WHITE
        elif Castle.YELLOW.value in somestr:
            return Castle.YELLOW
        elif Icons.LES.value in somestr:
            return Castle.LES
        elif Icons.GORY.value in somestr:
            return Castle.GORY
        return Castle.UNDEFINED

    def serialize(self):
        char_dict = {'name': self.name, 'prof': self.prof, 'stamina': self.stamina, 'level': self.level,
                     'attack': self.attack, 'defence': self.defence, 'equip': self.equip, 'backpack': self.backpack,
                     'stockSize': self.stockSize, 'stock': self.stock, 'exp': self.exp, 'needExp': self.needExp,
                     'arenaWins': self.arenaWins, 'arenaMax': self.arenaMax, 'arenaWalked': self.arenaWalked,
                     'castle': self.castle.value, 'alliance': self.alliance.value,
                     'pet': self.pet.serialize() if self.pet else None, 'config': self.config.serialize(),
                     'timers': self.timers.serialize(), 'maxStamina': self.maxStamina}
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
            self.alliance = Castle(char_dict['alliance'])
        if 'pet' in keys and char_dict['pet']:
            self.pet = Pet.deserialize(char_dict['pet'])
        if 'config' in keys and char_dict['config']:
            self.config = Configuration.deserialize(char_dict['config'])
        if 'timers' in keys and char_dict['timers']:
            self.timers = Timers.deserialize(char_dict['timers'])
        if 'maxStamina' in keys:
            self.maxStamina = char_dict['maxStamina']

