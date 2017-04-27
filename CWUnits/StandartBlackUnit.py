# -*- coding: utf-8 -*-
from CWUnits.BaseUnit import *
from telethon import TelegramClient
from telethon.tl.functions.messages import GetInlineBotResultsRequest, SendInlineBotResultRequest, ForwardMessageRequest
from telethon.utils import get_input_peer
import telethon.helpers as utils
from enums import *
from random import randint
from Character import Character
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage, UpdatesTg, UpdateNewChannelMessage, \
    UpdateNewMessage, Message
import re
import regexp
import enums
from pytz import timezone
import time as t
from time import sleep


class Module(BaseUnit):
    _timezone = timezone('Europe/Moscow')

    _captchaMsg = ''
    _statusBeforeCaptcha = CharacterStatus.UNDEFINED
    
    def __init__(self, tg_client: TelegramClient, character: Character):
        super().__init__(tg_client, character)

    def _send_captcha(self, captcha):
        self._append_to_send_queue(self._cwBot, captcha)

    def _send_order(self, order):
        if order[0] == CharacterAction.ATTACK:
            result = self._tgClient.invoke(
                GetInlineBotResultsRequest(get_input_peer(self._orderBot),
                                           get_input_peer(self._cwBot),
                                           '', ''))
            res = self._find_inline_by_title(result.results, 'Атака')
            self._tgClient.invoke(
                SendInlineBotResultRequest(get_input_peer(self._cwBot),
                                           utils.generate_random_long(),
                                           result.query_id, res.id))
            self._send_castle(order[1])
        elif order[0] == CharacterAction.DEFENCE:
            result = self._tgClient.invoke(
                GetInlineBotResultsRequest(get_input_peer(self._orderBot),
                                           get_input_peer(self._cwBot),
                                           '', ''))
            res = self._find_inline_by_title(result.results, 'Защита')
            self._tgClient.invoke(
                SendInlineBotResultRequest(get_input_peer(self._cwBot),
                                           utils.generate_random_long(),
                                           result.query_id, res.id))
            self._send_castle(order[1])
        elif order[0] == CharacterAction.QUEST:
            self._append_to_send_queue(self._cwBot, Buttons.QUEST.value)
            self._append_to_send_queue(self._cwBot, order[1].value)
        elif order[0] == CharacterAction.CAPTCHA:
            self._append_to_send_queue(self._captchaBot, order[1])
        elif order[0] == CharacterAction.GET_DATA:
            self._append_to_send_queue(self._cwBot, order[1].value)

    def _send_castle(self, castle):
        sleep(random() * 2 + 1)
        result = self._tgClient.invoke(
            GetInlineBotResultsRequest(get_input_peer(self._orderBot),
                                       get_input_peer(self._cwBot),
                                       '', ''))
        res = result.results[0]
        if castle == Castle.BLACK:
            res = self._find_inline_by_title(result.results, 'Черный замок')
        elif castle == Castle.BLUE:
            res = self._find_inline_by_title(result.results, 'Синий замок')
        elif castle == Castle.RED:
            res = self._find_inline_by_title(result.results, 'Красный замок')
        elif castle == Castle.YELLOW:
            res = self._find_inline_by_title(result.results, 'Желтый замок')
        elif castle == Castle.WHITE:
            res = self._find_inline_by_title(result.results, 'Белый замок')
        elif castle == Castle.LES:
            res = self._find_inline_by_title(result.results, 'Лесной форт')
        elif castle == Castle.GORY:
            res = self._find_inline_by_title(result.results, 'Горный форт')
        self._tgClient.invoke(
            SendInlineBotResultRequest(get_input_peer(self._cwBot),
                                       utils.generate_random_long(),
                                       result.query_id, res.id))

    @staticmethod
    def _find_inline_by_title(inline_results, title):
        for res in inline_results:
            if res.title == title:
                return res

    def _action(self):
        if self._character.status == CharacterStatus.NEED_CAPTCHA:
            self._send_order([self._character.status.value, self._captchaMsg])
        elif self._character.needProfile and self._character.status != CharacterStatus.WAITING_DATA_CHARACTER:
            self._character.status = CharacterStatus.WAITING_DATA_CHARACTER
            self._send_order(self._character.status.value)
        elif self._character.time_to_sleep():
            self._send_order([CharacterAction.WAIT])
        elif self._character.time_to_battle() and self._character.status.value != self._character.currentOrder and \
                self._character.config.autoBattle:
            self._character.status = CharacterStatus(self._character.currentOrder)
            self._send_order(self._character.status.value)
        elif (self._character.status.value[0] == CharacterAction.ATTACK or
                self._character.status.value[0] == CharacterAction.DEFENCE) and \
                not self._character.time_to_battle():
            self._character.status = CharacterStatus.REST
            self._currentOrder = [CharacterAction.DEFENCE, self._character.castle]
        elif self._character.status == CharacterStatus.REST:
            if self._character.needLevelUp and self._character.config.autoLevelUp:
                self._append_to_send_queue(self._cwBot, enums.Buttons.LEVEL_UP)
                if self._character.config.levelUpAtk:
                    self._append_to_send_queue(self._cwBot, enums.Buttons.UP_ATTACK)
                else:
                    self._append_to_send_queue(self._cwBot, enums.Buttons.UP_DEFENCE)
                self._character.needLevelUp = False
            if self._character.config.autoQuest and self._character.timers.lastProfileUpdate + 3600 < t.time():
                self._character.status = CharacterStatus.WAITING_DATA_CHARACTER
                self._send_order(self._character.status.value)
            elif self._character.config.autoQuest and \
                    (self._character.stamina >= 1 and self._character.config.defaultQuest == Quest.LES or
                     self._character.stamina >= 2 and (self._character.config.defaultQuest == Quest.CAVE or
                                                       self._character.config.defaultQuest == Quest.COW)):
                self._character.timers.lastQuest = t.time() + randint(10, 180)
                self._character.status = CharacterStatus([CharacterAction.QUEST, self._character.config.defaultQuest])
                self._character.stamina -= 1 if self._character.config.defaultQuest == Quest.LES else 2
                self._character.save_config_file()
                self._send_order(self._character.status.value)
    
    def parse_message(self, message):
        if re.search(regexp.main_hero, message):
            print('Получили профиль')
            self._character.parse_profile(message)
        elif re.search(regexp.captcha, message):
            print('Словили капчу =(')
            if re.search(regexp.captcha, message).group(1):
                self._captchaMsg = str(re.search(regexp.captcha, message).group(1))
            self._statusBeforeCaptcha = self._character.status
            self._character.status = CharacterStatus.NEED_CAPTCHA
        elif re.search(regexp.uncaptcha, message):
            print('Решили капчу =)')
            self._captchaMsg = ''
            self._character.status = self._statusBeforeCaptcha
        elif self._character.status in (CharacterStatus.QUEST_LES,
                                        CharacterStatus.QUEST_CAVE,
                                        CharacterStatus.QUEST_COW) \
                and t.time() + 180 - self._character.timers.lastQuest > 60*5:
            print('Вероятно вернулись с квеста')
            self._character.status = CharacterStatus.REST

    def _receive(self, msg):
        if type(msg) is UpdatesTg:
            for upd in msg.updates:
                if type(upd) is UpdateNewChannelMessage:
                    message = upd.message
                    if type(message) is Message:
                        channel = None
                        for chat in msg.chats:
                            if chat.id == message.to_id.channel_id:
                                channel = chat
                        if message.out:
                            pass
                        else:
                            if channel and self._channel_in_list(channel):
                                if self._can_order_id(message.from_id):
                                    self._character.set_order(message.message)
                elif type(upd) is UpdateNewMessage:
                    message = upd.message
                    if type(message) is Message:
                        if message.out:
                            if message.to_id.user_id == message.from_id:
                                self._character.set_order(message.message)
                        elif self._id_in_list(message.from_id):
                            if self._can_order_id(message.from_id):
                                print('Получли приказ')
                                self._character.set_order(message.message)
                            elif message.from_id == self._cwBot.id:
                                print('Получили сообщение от ChatWars')
                                if re.search(regexp.main_hero, message.message):
                                    self._tgClient.invoke(ForwardMessageRequest(get_input_peer(self._dataBot),
                                                                                message.id,
                                                                                utils.generate_random_long()))
                                self.parse_message(message.message)
                            elif message.from_id == self._captchaBot.id:
                                print('Получили сообщение от капчебота, пересылаем в ChatWars')
                                self._send_captcha(message.message)
        elif type(msg) is UpdateShortMessage:
            if msg.out:
                print('You sent {} to user #{}'.format(msg.message,
                                                       msg.user_id))
            elif self._id_in_list(msg.user_id):
                if self._can_order_id(msg.user_id):
                    print('Получли приказ')
                    self._character.set_order(msg.message)
                elif msg.user_id == self._cwBot.id:
                    print('Получили сообщение от ChatWars')
                    self.parse_message(msg.message)
                elif msg.user_id == self._captchaBot.id:
                    print('Получили сообщение от капчебота, пересылаем в ChatWars')
                    self._send_captcha(msg.message)

        elif type(msg) is UpdateShortChatMessage:
            if msg.out:
                print('You sent {} to chat #{}'.format(msg.message,
                                                       msg.chat_id))
            elif self._id_in_list(msg.from_id):
                print('[Chat #{}, user #{} sent {}]'.format(
                    msg.chat_id, msg.from_id,
                    msg.message))
