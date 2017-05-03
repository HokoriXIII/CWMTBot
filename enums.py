# -*- coding: utf-8 -*-
from enum import Enum


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
    CHARACTER = '🏅Герой'
    HERO = '/hero'
    PET = '/pet'
    STOCK = '/stock'
    INV = '/inv'


class Castle(Enum):
    UNDEFINED = 0
    BLACK = '🇬🇵'
    RED = '🇮🇲'
    BLUE = '🇪🇺'
    YELLOW = '🇻🇦'
    WHITE = '🇨🇾'
    MINT = '🇲🇴'
    DUSK = '🇰🇮'
    LES = '🌲Лесной форт'
    GORY = '⛰Горный форт'

    def __str__(self):
        return self.value


class Icons(Enum):
    BLACK = '🇬🇵'
    RED = '🇮🇲'
    BLUE = '🇪🇺'
    YELLOW = '🇻🇦'
    WHITE = '🇨🇾'
    MINT = '🇲🇴'
    DUSK = '🇰🇮'
    LES = '🌲'
    GORY = '⛰'


class StatusText(Enum):
    REST = '🛌Отдых'
    ATTACK = 'Атака'
    DEFENCE = 'Защита'
    LES = 'В лесу'
    CAVE = 'В пещере'
    COW = 'Возишься с КОРОВАНАМИ'
    ARENA = 'На арене'


class Quest(Enum):
    LES = '🌲Лес'
    CAVE = '🕸Пещера'
    COW = '🐫ГРАБИТЬ КОРОВАНЫ'


class CharacterStatus(Enum):
    UNDEFINED = 0
    REST = [CharacterAction.WAIT, 0]
    QUEST_LES = [CharacterAction.QUEST, Quest.LES]
    QUEST_CAVE = [CharacterAction.QUEST, Quest.CAVE]
    QUEST_COW = [CharacterAction.QUEST, Quest.COW]
    ATTACK_BLACK = [CharacterAction.ATTACK, Castle.BLACK]
    ATTACK_RED = [CharacterAction.ATTACK, Castle.RED]
    ATTACK_BLUE = [CharacterAction.ATTACK, Castle.BLUE]
    ATTACK_YELLOW = [CharacterAction.ATTACK, Castle.YELLOW]
    ATTACK_WHITE = [CharacterAction.ATTACK, Castle.WHITE]
    ATTACK_LES = [CharacterAction.ATTACK, Castle.LES]
    ATTACK_GORY = [CharacterAction.ATTACK, Castle.GORY]
    ATTACK_UNDEFINED = [CharacterAction.ATTACK, Castle.UNDEFINED]
    DEFENCE_BLACK = [CharacterAction.DEFENCE, Castle.BLACK]
    DEFENCE_RED = [CharacterAction.DEFENCE, Castle.RED]
    DEFENCE_BLUE = [CharacterAction.DEFENCE, Castle.BLUE]
    DEFENCE_YELLOW = [CharacterAction.DEFENCE, Castle.YELLOW]
    DEFENCE_WHITE = [CharacterAction.DEFENCE, Castle.WHITE]
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


class Buttons(Enum):
    QUEST = '🗺 Квесты'
    LEVEL_UP = '/level_up'
    UP_ATTACK = '+1 ⚔Атака'
    UP_DEFENCE = '+1 🛡Защита'
    FEED_PET = '🍼Покормить'
    PLAY_PET = '⚽️Поиграть'
    CLEAN_PET = '🛁Почистить'


class PetStatusText(Enum):
    EXCELLENT = 'отлично!'
