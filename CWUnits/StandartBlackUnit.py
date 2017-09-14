# -*- coding: utf-8 -*-
from CWUnits.BaseUnit import *
from telethon import TelegramClient
from telethon.tl.functions.messages import GetInlineBotResultsRequest, SendInlineBotResultRequest, ForwardMessageRequest
from telethon.utils import get_input_peer
import telethon.helpers as utils
from enums import *
import random
from Character import Character
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage, Updates, UpdateNewChannelMessage, \
    UpdateNewMessage, Message
import re
import regexp
import enums
from datetime import datetime, timedelta
from pytz import timezone
import time as t
from time import sleep


class Module(BaseUnit):
    _timezone = timezone('Europe/Moscow')

    _captchaMsg = ''
    _statusBeforeCaptcha = CharacterStatus.UNDEFINED
    _next_build_try = datetime.now()
    
    def __init__(self, tg_client: TelegramClient, character: Character):
        super().__init__(tg_client, character)

    def _send_captcha(self, captcha):
        self._append_to_send_queue(self._cwBot, captcha)

    def _send_order(self, order):
        if order[0] == CharacterAction.ATTACK:
            self._append_to_send_queue(self._cwBot, enums.Buttons.ATTACK.value)
            self._append_to_send_queue(self._cwBot, order[1].value)
        elif order[0] == CharacterAction.DEFENCE:
            self._append_to_send_queue(self._cwBot, enums.Buttons.DEFENCE.value)
            self._append_to_send_queue(self._cwBot, order[1].value)
        elif order[0] == CharacterAction.QUEST:
            self._append_to_send_queue(self._cwBot, Buttons.QUEST.value)
            self._append_to_send_queue(self._cwBot, order[1].value)
        elif order[0] == CharacterAction.CAPTCHA:
            self._append_to_send_queue(self._captchaBot, order[1])
        elif order[0] == CharacterAction.GET_DATA:
            self._append_to_send_queue(self._cwBot, order[1].value)
        elif order[0] == CharacterAction.BUILD:
            self._append_to_send_queue(self._cwBot, order[1])

    @staticmethod
    def _find_inline_by_title(inline_results, title):
        for res in inline_results:
            if res.title == title:
                return res

    def _action(self):
        if self._character.status == CharacterStatus.PAUSED:
            return
        if self._character.status == CharacterStatus.NEED_CAPTCHA:
            self._send_order([self._character.status.value, self._captchaMsg])
            self._character.status = CharacterStatus.WAITING_CAPTCHA
        elif self._character.needProfile and self._character.status != CharacterStatus.WAITING_DATA_CHARACTER:
            self._character.status = CharacterStatus.WAITING_DATA_CHARACTER
            self._send_order(self._character.status.value)
        elif self._character.time_to_sleep():
            self._send_order([CharacterAction.WAIT])
        elif self._character.time_to_battle() and self._character.status.value \
                not in (self._character.currentOrder,
                        CharacterStatus.QUEST_COW.value,
                        CharacterStatus.QUEST_CAVE.value,
                        CharacterStatus.QUEST_LES.value) \
                and self._character.status.value[0] not in [CharacterAction.BUILD] \
                and self._character.config.autoBattle:
            self._character.status = CharacterStatus(self._character.currentOrder)
            self._send_order(self._character.status.value)
        elif (self._character.status.value[0] == CharacterAction.ATTACK or
                self._character.status.value[0] == CharacterAction.DEFENCE) and \
                not self._character.time_to_battle():
            self._character.status = CharacterStatus.REST
            self._append_to_send_queue(self._cwBot, '/report')
            self._character.set_order(self._character.castle.value)
        elif self._character.status == CharacterStatus.REST:
            if self._character.needLevelUp and self._character.config.autoLevelUp:
                self._append_to_send_queue(self._cwBot, enums.Buttons.LEVEL_UP.value)
                if self._character.config.levelUpAtk:
                    self._append_to_send_queue(self._cwBot, enums.Buttons.UP_ATTACK.value)
                else:
                    self._append_to_send_queue(self._cwBot, enums.Buttons.UP_DEFENCE.value)
                self._character.needLevelUp = False
            elif self._character.needPetRequest and self._character.status != CharacterStatus.WAITING_DATA_PET:
                self._character.status = CharacterStatus.WAITING_DATA_PET
                self._send_order(self._character.status.value)
            elif self._character.needCleanPet:
                self._append_to_send_queue(self._cwBot, enums.Buttons.CLEAN_PET.value)
                self._character.needCleanPet = False
            elif self._character.needPlayPet:
                self._append_to_send_queue(self._cwBot, enums.Buttons.PLAY_PET.value)
                self._character.needPlayPet = False
            elif self._character.needFeedPet:
                self._append_to_send_queue(self._cwBot, enums.Buttons.FEED_PET.value)
                self._character.needFeedPet = False
            elif self._character.config.autoQuest and self._character.timers.lastProfileUpdate + 3600 < t.time():
                self._character.status = CharacterStatus.WAITING_DATA_CHARACTER
                self._send_order(self._character.status.value)
            elif self._character.config.autoQuest and \
                    (self._character.stamina >= 1 and (self._character.config.defaultQuest == Quest.LES or
                                                       self._character.level < 7 and
                                                       self._character.config.defaultQuest == Quest.CAVE) or
                     self._character.stamina >= 2 and (self._character.config.defaultQuest == Quest.CAVE or
                                                       self._character.config.defaultQuest == Quest.COW)):
                self._character.timers.lastQuest = t.time()
                if self._character.level < 7 and self._character.config.defaultQuest == Quest.CAVE:
                    self._character.status = CharacterStatus([CharacterAction.QUEST, Quest.LES])
                    self._character.stamina -= 1
                else:
                    self._character.status = CharacterStatus(
                        [CharacterAction.QUEST, self._character.config.defaultQuest])
                    self._character.stamina -= 1 if self._character.config.defaultQuest == Quest.LES else 2
                self._character.save_config_file()
                self._send_order(self._character.status.value)
            elif self._character.config.autoBuild and self._character.gold >= 5 and len(self._character.actualBuild) \
                    and self._next_build_try < datetime.now():
                self._character.status = CharacterStatus(
                    [CharacterAction.BUILD, random.choice(self._character.actualBuild)])
                self._character.save_config_file()
                self._send_order(self._character.status.value)
    
    def parse_message(self, message):
        if re.search(regexp.main_hero, message):
            print(str(datetime.now()) + ': ' + 'Получили профиль')
            self._character.parse_profile(message)
        elif re.search(regexp.pet, message):
            print(str(datetime.now()) + ': ' + 'Получили пета')
            self._character.parse_pet(message)
        elif re.search(regexp.captcha, message):
            print(str(datetime.now()) + ': ' + 'Словили капчу =(')
            if re.search(regexp.captcha, message).group(1):
                self._captchaMsg = str(re.search(regexp.captcha, message).group(1))
            self._statusBeforeCaptcha = self._character.status
            self._character.status = CharacterStatus.NEED_CAPTCHA
        elif re.search(regexp.uncaptcha, message):
            print(str(datetime.now()) + ': ' + 'Решили капчу =)')
            self._captchaMsg = ''
            self._character.status = self._statusBeforeCaptcha
        elif self._character.status in (CharacterStatus.QUEST_LES,
                                        CharacterStatus.QUEST_CAVE,
                                        CharacterStatus.QUEST_COW) \
                and t.time() + 15 - self._character.timers.lastQuest > 60*5:
            print(str(datetime.now()) + ': ' + 'Вероятно вернулись с квеста')
            self._character.status = CharacterStatus.REST

    def _on_cw_msg(self, message):
        print(str(datetime.now()) + ': ' + 'Получили сообщение от ChatWars')
        if self._character.status == CharacterStatus.PAUSED:
            return
        if re.search(regexp.main_hero, message.message):
            self._tgClient.invoke(ForwardMessageRequest(get_input_peer(self._dataBot),
                                                        message.id,
                                                        utils.generate_random_long()))
        if '/fight_' in message.message:
            self._tgClient.invoke(ForwardMessageRequest(
                get_input_peer(self._dataBot),
                message.id,
                utils.generate_random_long()
            ))
        if 'Ты вернулся со стройки:' in message.message or 'Здание отремонтировано:' in message.message:
            self._tgClient.invoke(ForwardMessageRequest(
                get_input_peer(self._dataBot),
                message.id,
                utils.generate_random_long()
            ))
            print(str(datetime.now()) + ': ' + 'Вернулись из стройки')
            self._next_build_try = datetime.now() + timedelta(minutes=random.randint(0, 2),
                                                              seconds=random.randint(0, 59))
            self._character.status = CharacterStatus.REST
        if 'В казне недостаточно ресурсов' in message.message:
            print(str(datetime.now()) + ': ' + 'Стройка не удалась')
            self._character.status = CharacterStatus.REST
            self._next_build_try = datetime.now() + timedelta(minutes=random.randint(1, 4),
                                                              seconds=random.randint(0, 59))
        if 'Твои результаты в бою:' in message.message:
            self._tgClient.invoke(ForwardMessageRequest(
                get_input_peer(self._dataBot),
                message.id,
                utils.generate_random_long()
            ))
        self.parse_message(message.message)

    def _receive(self, msg):
        if type(msg) is Updates:
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
                                    Thread(target=self._order_recieved, name='on_cw_msg', args=(message,)).start()
                elif type(upd) is UpdateNewMessage:
                    message = upd.message
                    if type(message) is Message:
                        if message.out:
                            if message.to_id.user_id == message.from_id:
                                self._character.set_order(message.message)
                        elif self._id_in_list(message.from_id):
                            if self._can_order_id(message.from_id):
                                Thread(target=self._order_recieved, name='on_cw_msg', args=(message,)).start()
                            elif message.from_id == self._cwBot.id:
                                Thread(target=self._on_cw_msg, name='on_cw_msg', args=(message,)).start()
                            elif message.from_id == self._captchaBot.id:
                                print(str(datetime.now()) + ': ' + 'Получили сообщение от капчебота, пересылаем в ChatWars')
                                self._send_captcha(message.message)
                            elif message.from_id == self._dataBot.id:
                                if re.search(regexp.build, message.message):
                                    print(str(datetime.now()) + ': ' + 'Получили стройку')
                                    self._character.parse_build(message.message)
        elif type(msg) is UpdateShortMessage:
            if msg.out:
                print(str(datetime.now()) + ': ' + 'You sent {} to user #{}'.format(msg.message,
                                                       msg.user_id))
            elif self._id_in_list(msg.user_id):
                if self._can_order_id(msg.user_id):
                    Thread(target=self._order_recieved, name='on_cw_msg', args=(msg,)).start()
                elif msg.user_id == self._cwBot.id:
                    Thread(target=self._on_cw_msg, name='on_cw_msg', args=(msg,)).start()
                elif msg.user_id == self._captchaBot.id:
                    print(str(datetime.now()) + ': ' + 'Получили сообщение от капчебота, пересылаем в ChatWars')
                    self._send_captcha(msg.message)

        elif type(msg) is UpdateShortChatMessage:
            if msg.out:
                print(str(datetime.now()) + ': ' + 'You sent {} to chat #{}'.format(msg.message,
                                                       msg.chat_id))
            elif self._id_in_list(msg.from_id):
                print(str(datetime.now()) + ': ' + '[Chat #{}, user #{} sent {}]'.format(msg.chat_id, msg.from_id, msg.message))
                if msg.from_id == self._cwBot.id:
                    Thread(target=self._on_cw_msg, name='on_cw_msg', args=(msg,)).start()

    def _order_recieved(self, message):
        print(str(datetime.now()) + ': ' + 'Получли приказ')
        if re.search(regexp.build, message.message):
            print(str(datetime.now()) + ': ' + 'Получили стройку')
            self._character.parse_build(message.message)
        elif message.message.upper() == 'Стопэ'.upper():
            self._character.status = CharacterStatus.PAUSED
            self._tgClient.send_message(self._admin, 'Сделаль')
        elif message.message.upper() == 'Продолжай'.upper():
            self._character.status = CharacterStatus.UNDEFINED
            self._character.needProfile = True
            self._tgClient.send_message(self._admin, 'Сделаль')
        else:
            self._character.set_order(message.message)
