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


class Castle(Enum):
    UNDEFINED = 0
    BLACK = '🇬🇵'
    RED = '🇮🇲'
    BLUE = '🇪🇺'
    YELLOW = '🇻🇦'
    WHITE = '🇨🇾'
    LES = '🌲Лесной форт'
    GORY = '⛰Горный форт'


class Icons(Enum):
    BLACK = '🇬🇵'
    RED = '🇮🇲'
    BLUE = '🇪🇺'
    YELLOW = '🇻🇦'
    WHITE = '🇨🇾'
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


class CharacterStatus(Enum):
    UNDEFINED = 0
    REST = 1
    QUEST_LES = 2
    QUEST_CAVE = 3
    QUEST_COW = 4
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
    ARENA = 15
    CRAFTING = 16
    WAITING_DATA = 17


class Quest(Enum):
    LES = '🌲Лес'
    CAVE = '🕸Пещера'
    COW = '🐫ГРАБИТЬ КОРОВАНЫ'


class Buttons(Enum):
    QUEST = '🗺 Квесты'
