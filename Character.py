# -*- coding: utf-8 -*-
from pathlib import Path
import json
import time as t
import re
import regexp
from datetime import datetime, time
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
    autoArena = False
    autoQuest = False
    defaultQuest = Quest.LES
    autoBattle = False
    autoDonate = False
    donateTill = 0
    autoPet = False
    autoCaptcha = False
    autoCraft = False
    autoEquip = False
    autoTrade = False
    autoLevelUp = False
    # Если levelUpAtk True, то уровень будет вкачиваться в атаку, если False в защиту.
    levelUpAtk = True
    orderBot = ''
    orderChat = ''
    dataBot = ''
    admin = ''
    module = ''
    sleep_intervals = [[[0, 10], [3, 50]],
                       [[4, 15], [7, 45]]]

    def serialize(self):
        conf_dict = {'autoArena': self.autoArena, 'autoQuest': self.autoQuest, 'autoBattle': self.autoBattle,
                     'autoDonate': self.autoDonate, 'donateTill': self.donateTill, 'autoPet': self.autoPet,
                     'autoCaptcha': self.autoCaptcha, 'autoCraft': self.autoCraft, 'autoEquip': self.autoEquip,
                     'autoTrade': self.autoTrade, 'autoLevelUp': self.autoLevelUp, 'levelUpAtk': self.levelUpAtk,
                     'defaultQuest': self.defaultQuest.value, 'orderBot': self.orderBot, 'orderChat': self.orderChat,
                     'dataBot': self.dataBot, 'admin': self.admin, 'module': self.module,
                     'sleep_intervals': self.sleep_intervals}
        return conf_dict

    @staticmethod
    def deserialize(conf_dict):
        conf_keys = conf_dict.keys()
        conf = Configuration()
        if 'autoArena' in conf_keys:
            conf.autoArena = conf_dict['autoArena']
        if 'autoQuest' in conf_keys:
            conf.autoQuest = conf_dict['autoQuest']
        if 'autoBattle' in conf_keys:
            conf.autoBattle = conf_dict['autoBattle']
        if 'autoDonate' in conf_keys:
            conf.autoDonate = conf_dict['autoDonate']
        if 'donateTill' in conf_keys:
            conf.donateTill = conf_dict['donateTill']
        if 'autoPet' in conf_keys:
            conf.autoPet = conf_dict['autoPet']
        if 'autoCaptcha' in conf_keys:
            conf.autoCaptcha = conf_dict['autoCaptcha']
        if 'autoCraft' in conf_keys:
            conf.autoCraft = conf_dict['autoCraft']
        if 'autoEquip' in conf_keys:
            conf.autoEquip = conf_dict['autoEquip']
        if 'autoTrade' in conf_keys:
            conf.autoTrade = conf_dict['autoTrade']
        if 'autoLevelUp' in conf_keys:
            conf.autoLevelUp = conf_dict['autoLevelUp']
        if 'levelUpAtk' in conf_keys:
            conf.levelUpAtk = conf_dict['levelUpAtk']
        if 'defaultQuest' in conf_keys:
            conf.defaultQuest = Quest(conf_dict['defaultQuest'])
        if 'orderBot' in conf_keys:
            conf.orderBot = conf_dict['orderBot']
        if 'orderChat' in conf_keys:
            conf.orderChat = conf_dict['orderChat']
        if 'dataBot' in conf_keys:
            conf.dataBot = conf_dict['dataBot']
        if 'admin' in conf_keys:
            conf.admin = conf_dict['admin']
        if 'module' in conf_keys:
            conf.module = conf_dict['module']
        if 'sleep_intervals' in conf_keys:
            conf.sleep_intervals = conf_dict['sleep_intervals']
        return conf


class Timers:
    lastArenaEnd = 0.0
    lastQuest = 0.0
    lastProfileUpdate = 0.0
    lastStockUpdate = 0.0
    lastEquipUpdate = 0.0

    def serialize(self):
        time_dict = {'lastQuest': self.lastQuest, 'lastProfileUpdate': self.lastProfileUpdate,
                     'lastArenaEnd': self.lastArenaEnd, 'lastStockUpdate': self.lastStockUpdate,
                     'lastEquipUpdate': self.lastEquipUpdate}
        return time_dict

    @staticmethod
    def deserialize(timers_dict):
        timers = Timers()
        keys = timers_dict.keys()
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
    alliance = []
    status = CharacterStatus.UNDEFINED
    config = Configuration()
    timers = Timers()
    gold = 0
    donateGold = 0

    needProfile = False
    _needHeroRequest = False
    needPetRequest = False
    _needStockRequest = False
    _needInvRequest = False
    needLevelUp = False
    needFeedPet = False
    needCleanPet = False
    needPlayPet = False

    _BATTLE_TIME = [[time(3, 45), time(4, 5)],
                    [time(7, 45), time(8, 5)],
                    [time(11, 45), time(12, 5)],
                    [time(15, 45), time(16, 5)],
                    [time(19, 45), time(20, 5)],
                    [time(23, 45), time(0, 5)]]

    def __init__(self, client):
        # self._client = client
        self._name = client
        self._config_file = Path(self._name + '.character')
        if self._config_file.is_file():
            self.reload_config_file()
        self.needProfile = True
        self.currentOrder = [CharacterAction.DEFENCE, self.castle]

    def set_opts(self, opts):
        for opt, arg in opts:
            if opt in ('-m', '--module'):
                self.config.module = arg
            elif opt in ('-a', '--admin'):
                self.config.admin = arg
            elif opt in ('-o', '--order'):
                self.config.orderBot = arg
            elif opt in ('-c', '--chat'):
                self.config.orderChat = arg
            elif opt in ('-d', '--data'):
                self.config.dataBot = arg

    def reload_config_file(self):
        self.deserialize(self._config_file.read_text('utf8'))

    def save_config_file(self):
        config = self.serialize()
        self._config_file.write_text(config, 'utf8')

    def time_to_sleep(self):
        now = datetime.now().time()
        for interval in self.config.sleep_intervals:
            time_start = time(interval[0][0], interval[0][1])
            time_end = time(interval[1][0], interval[1][1])
            if time_start <= time_end and time_start <= now <= time_end or \
                    not time_start <= time_end and (time_start <= now or now <= time_end):
                return True
        return False

    def time_to_battle(self):
        now = datetime.now().time()
        for time_start, time_end in self._BATTLE_TIME:
            if time_start <= time_end and time_start <= now <= time_end or \
                            not time_start <= time_end and (time_start <= now or now <= time_end):
                return True
        return False

    def set_order(self, target):
        try:
            if Castle(target) == self.castle or Castle(target) in self.alliance:
                order = CharacterAction.DEFENCE
            else:
                order = CharacterAction.ATTACK
            self.currentOrder = [order, Castle(target)]
        except ValueError:
            pass

    def parse_pet(self, pet):
        self.pet = Pet()
        parsed_data = re.search(regexp.pet, pet)
        if parsed_data.group(2):
            self.pet.name = str(parsed_data.group(2))
        self.pet.race = str(parsed_data.group(3))
        self.pet.level = int(parsed_data.group(4))
        self.pet.exp = int(parsed_data.group(5))
        self.pet.needExp = int(parsed_data.group(6))
        self.pet.playStatus = str(parsed_data.group(7))
        self.pet.eatStatus = str(parsed_data.group(8))
        self.pet.bathStatus = str(parsed_data.group(9))
        self.pet.foodInStock = int(parsed_data.group(10))
        self.pet.profit = str(parsed_data.group(11))
        self.save_config_file()
        if self.pet.playStatus != PetStatusText.EXCELLENT.value:
            self.needPlayPet = True
        if self.pet.eatStatus != PetStatusText.EXCELLENT.value:
            self.needFeedPet = True
        if self.pet.bathStatus != PetStatusText.EXCELLENT.value:
            self.needCleanPet = True
        self.needPetRequest = False
        self.status = CharacterStatus.REST

    def parse_profile(self, profile):
        self.needProfile = False
        parsed_data = re.search(regexp.main_hero, profile)
        if parsed_data.group(1):
            self.needLevelUp = True
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
                and str(parsed_data.group(16)) != '[-]' \
                and int(parsed_data.group(17)) != 0:
            self._needInvRequest = True
        if parsed_data.group(19) and (not self.pet or str(parsed_data.group(20)) != '😁'):
            self.needPetRequest = True
        self.status = self._parse_status(parsed_data.group(23))
        self.timers.lastProfileUpdate = t.time() + randint(50, 3600)
        self.save_config_file()
        if self.currentOrder[1] == Castle.UNDEFINED:
            self.currentOrder = [CharacterAction.DEFENCE, self.castle]

    def _parse_status(self, status):
        if StatusText.REST.value in status:
            return CharacterStatus.REST
        elif StatusText.ARENA.value in status:
            return CharacterStatus.ARENA
        elif StatusText.ATTACK.value in status:
            castle = self._find_castle(status)
            return CharacterStatus([CharacterAction.ATTACK, castle])
        elif StatusText.DEFENCE.value in status:
            castle = self._find_castle(status)
            return CharacterStatus([CharacterAction.DEFENCE, castle])
        elif StatusText.LES.value in status:
            return CharacterStatus.QUEST_LES
        elif StatusText.CAVE.value in status:
            return CharacterStatus.QUEST_CAVE
        elif StatusText.COW.value in status:
            return CharacterStatus.QUEST_COW
        return CharacterStatus.UNDEFINED

    @staticmethod
    def _find_castle(somestr):
        if Icons.BLACK.value in somestr:
            return Castle.BLACK
        elif Icons.BLUE.value in somestr:
            return Castle.BLUE
        elif Icons.RED.value in somestr:
            return Castle.RED
        elif Icons.WHITE.value in somestr:
            return Castle.WHITE
        elif Icons.YELLOW.value in somestr:
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
                     'castle': self.castle.value, 'alliance': self.alliance,
                     'pet': self.pet.serialize() if self.pet else None, 'config': self.config.serialize(),
                     'timers': self.timers.serialize(), 'maxStamina': self.maxStamina}
        return json.dumps(char_dict, ensure_ascii=False, indent=4)

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
            self.status = CharacterStatus(char_dict['status'])
        if 'castle' in keys:
            self.castle = Castle(char_dict['castle'])
        if 'alliance' in keys:
            self.alliance = char_dict['alliance']
        if 'pet' in keys and char_dict['pet']:
            self.pet = Pet.deserialize(char_dict['pet'])
        if 'config' in keys and char_dict['config']:
            self.config = Configuration.deserialize(char_dict['config'])
        if 'timers' in keys and char_dict['timers']:
            self.timers = Timers.deserialize(char_dict['timers'])
        if 'maxStamina' in keys:
            self.maxStamina = char_dict['maxStamina']
