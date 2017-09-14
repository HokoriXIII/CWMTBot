# -*- coding: utf-8 -*-
from enum import Enum
#Unicode emoji from https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py

class CharacterAction(Enum):
    WAIT = 0
    QUEST = 1
    ATTACK = 2
    DEFENCE = 3
    ARENA = 4
    CRAFT = 5
    TRADE = 6
    GET_DATA = 7
    CAPTCHA = 8
    BUILD = 9


class PetType(Enum):
    PIG = '🐷'
    EVOK = '🙊'
    TONTON = ''
    HORSE = ''
    GOOSE = ''
    DONKEY = ''


class PetStatus(Enum):
    PERFECT = '😁'
    GOOD = '😃'
    NORMAL = '😐'
    BAD = '😢'
    DEAD = '☠'


class DataRequests(Enum):
    CHARACTER = '\U0001f3c5Герой'
    HERO = '/hero'
    PET = '/pet'
    STOCK = '/stock'
    INV = '/inv'


class Castle(Enum):
    UNDEFINED = 0
    BLACK = '\U0001f1ec\U0001f1f5'
    RED = '\U0001f1ee\U0001f1f2'
    BLUE = '\U0001f1ea\U0001f1fa'
    YELLOW = '\U0001f1fb\U0001f1e6'
    WHITE = '\U0001f1e8\U0001f1fe'
    MINT = '\U0001F1F2\U0001F1F4'
    DUSK = '\U0001F1F0\U0001F1EE'
    LES = '\U0001f332Лесной форт'
    GORY = '\u26f0Горный форт'
    SEA = '⚓️Морской форт'

    def __str__(self):
        return self.value


class Icons(Enum):
    BLACK = '\U0001f1ec\U0001f1f5'
    RED = '\U0001f1ee\U0001f1f2'
    BLUE = '\U0001f1ea\U0001f1fa'
    YELLOW = '\U0001f1fb\U0001f1e6'
    WHITE = '\U0001f1e8\U0001f1fe'
    MINT = '\U0001F1F2\U0001F1F4'
    DUSK = '\U0001F1F0\U0001F1EE'
    LES = '\U0001f332'
    GORY = '\u26f0'


class StatusText(Enum):
    REST = '🛌Отдых'
    ATTACK = 'Атака'
    DEFENCE = 'Защита'
    LES = 'В лесу'
    CAVE = 'В пещере'
    COW = 'Возишься с КОРОВАНАМИ'
    ARENA = 'На арене'


class Quest(Enum):
    LES = '\U0001f332Лес'
    CAVE = '\U0001f578Пещера'
    COW = '\U0001f42bГРАБИТЬ КОРОВАНЫ'


class CharacterStatus(Enum):
    UNDEFINED = [0]
    REST = [CharacterAction.WAIT, 0]
    QUEST_LES = [CharacterAction.QUEST, Quest.LES]
    QUEST_CAVE = [CharacterAction.QUEST, Quest.CAVE]
    QUEST_COW = [CharacterAction.QUEST, Quest.COW]
    ATTACK_BLACK = [CharacterAction.ATTACK, Castle.BLACK]
    ATTACK_RED = [CharacterAction.ATTACK, Castle.RED]
    ATTACK_BLUE = [CharacterAction.ATTACK, Castle.BLUE]
    ATTACK_YELLOW = [CharacterAction.ATTACK, Castle.YELLOW]
    ATTACK_WHITE = [CharacterAction.ATTACK, Castle.WHITE]
    ATTACK_MINT = [CharacterAction.ATTACK, Castle.MINT]
    ATTACK_DUSK = [CharacterAction.ATTACK, Castle.DUSK]
    ATTACK_LES = [CharacterAction.ATTACK, Castle.LES]
    ATTACK_GORY = [CharacterAction.ATTACK, Castle.GORY]
    ATTACK_UNDEFINED = [CharacterAction.ATTACK, Castle.UNDEFINED]
    DEFENCE_BLACK = [CharacterAction.DEFENCE, Castle.BLACK]
    DEFENCE_RED = [CharacterAction.DEFENCE, Castle.RED]
    DEFENCE_BLUE = [CharacterAction.DEFENCE, Castle.BLUE]
    DEFENCE_YELLOW = [CharacterAction.DEFENCE, Castle.YELLOW]
    DEFENCE_WHITE = [CharacterAction.DEFENCE, Castle.WHITE]
    DEFENCE_MINT = [CharacterAction.DEFENCE, Castle.MINT]
    DEFENCE_DUSK = [CharacterAction.DEFENCE, Castle.DUSK]
    DEFENCE_LES = [CharacterAction.DEFENCE, Castle.LES]
    DEFENCE_GORY = [CharacterAction.DEFENCE, Castle.GORY]
    DEFENCE_UNDEFINED = [CharacterAction.DEFENCE, Castle.UNDEFINED]
    ARENA = [CharacterAction.ARENA]
    CRAFTING = CharacterAction.CRAFT
    WAITING_DATA_CHARACTER = [CharacterAction.GET_DATA, DataRequests.CHARACTER]
    WAITING_DATA_HERO = [CharacterAction.GET_DATA, DataRequests.HERO]
    WAITING_DATA_PET = [CharacterAction.GET_DATA, DataRequests.PET]
    WAITING_DATA_INV = [CharacterAction.GET_DATA, DataRequests.INV]
    WAITING_DATA_STOCK = [CharacterAction.GET_DATA, DataRequests.STOCK]
    NEED_CAPTCHA = CharacterAction.CAPTCHA
    WAITING_CAPTCHA = [CharacterAction.WAIT, 1]
    BUILD_WALL = [CharacterAction.BUILD, '/build_wall']
    REPAIR_WALL = [CharacterAction.BUILD, '/repair_wall']
    BUILD_HQ = [CharacterAction.BUILD, '/build_hq']
    REPAIR_HQ = [CharacterAction.BUILD, '/repair_hq']
    BUILD_STASH = [CharacterAction.BUILD, '/build_stash']
    REPAIR_STASH = [CharacterAction.BUILD, '/repair_stash']
    BUILD_GLADIATORS = [CharacterAction.BUILD, '/build_gladiators']
    REPAIR_GLADIATORS = [CharacterAction.BUILD, '/repair_gladiators']
    BUILD_GOLDREWARD = [CharacterAction.BUILD, '/build_goldrewards2']
    REPAIR_GOLDREWARD = [CharacterAction.BUILD, '/repair_goldrewards2']
    BUILD_TEA = [CharacterAction.BUILD, '/build_teaparty']
    REPAIR_TEA = [CharacterAction.BUILD, '/repair_teaparty']
    BUILD_MONUMENT = [CharacterAction.BUILD, '/build_monument']
    REPAIR_MONUMENT = [CharacterAction.BUILD, '/repair_monument']
    BUILD_UNDEFINED = [CharacterAction.BUILD, '0']
    PAUSED = [-1]


class Buttons(Enum):
    QUEST = '\U0001f5fa Квесты'
    LEVEL_UP = '/level_up'
    UP_ATTACK = '+1 \u2694Атака'
    UP_DEFENCE = '+1 \U0001f6e1Защита'
    FEED_PET = '🍼Покормить'
    PLAY_PET = '\u26BDПоиграть'
    CLEAN_PET = '🛁Почистить'
    ATTACK = '\u2694 Атака'
    DEFENCE = '\U0001f6e1 Защита'


class PetStatusText(Enum):
    EXCELLENT = 'отлично!'
