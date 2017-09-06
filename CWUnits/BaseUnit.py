from abc import ABCMeta, abstractmethod
from telethon import TelegramClient
from Character import Character
from telethon.tl.types import User, Channel, Chat
from telethon.tl.functions.contacts import SearchRequest
import config
from multiprocessing import RLock
from time import sleep
from threading import Thread
from random import random


class BaseUnit(Thread):
    __metaclass__ = ABCMeta

    '''Хэндлер приёма сообщений'''
    @abstractmethod
    def _receive(self, msg):
        pass

    '''Процесс отправки действий, вызывается каждые 5-7 секунд'''
    @abstractmethod
    def _action(self):
        pass

    def __init__(self, tg_client: TelegramClient, character: Character):
        super().__init__()
        self._tgClient = tg_client
        self._character = character
        self._send_queue = []
        self._lock = RLock()
        self._dialogs = self._tgClient.get_dialogs(100)
        self._cwBot = self._find_contact_by_username(config.CWBot)
        if not self._cwBot:
            self._cwBot = self._tgClient.invoke(SearchRequest(config.CWBot, 1)).users[0]
            self._tgClient.send_message(self._cwBot, '/start')
            self._tgClient.send_message(self._cwBot, '🇬🇵Черный замок🇬🇵')
        self._captchaBot = self._find_contact_by_username(config.CaptchaBot)
        if not self._captchaBot:
            self._captchaBot = self._tgClient.invoke(SearchRequest(config.CaptchaBot, 1)).users[0]
            self._tgClient.send_message(self._captchaBot, '/start')
        self._tradeBot = self._find_contact_by_username(config.TradeBot)
        if not self._tradeBot:
            self._tradeBot = self._tgClient.invoke(SearchRequest(config.TradeBot, 1)).users[0]
            self._tgClient.send_message(self._tradeBot, '/start')
        self._orderBot = self._find_contact_by_username(self._character.config.orderBot)
        if not self._orderBot:
            self._orderBot = self._tgClient.invoke(SearchRequest(self._character.config.orderBot, 1)).users[0]
            self._tgClient.send_message(self._orderBot, '/start')
        self._dataBot = self._find_contact_by_username(self._character.config.dataBot)
        if not self._dataBot:
            self._dataBot = self._tgClient.invoke(SearchRequest(self._character.config.dataBot, 1)).users[0]
            self._tgClient.send_message(self._dataBot, '/start')
        self._admin = self._find_contact_by_username(self._character.config.admin)
        if not self._admin:
            self._admin = self._tgClient.invoke(SearchRequest(self._character.config.admin, 1)).users[0] if \
                len(self._tgClient.invoke(SearchRequest(self._character.config.admin, 1)).users) else None
        self._orderGroup = self._find_contact_by_name(self._character.config.orderChat)
        if not self._admin:
            # Если юзера-админа не нашли, то админим сами
            self._admin = self._tgClient.session.user
        self._tgClient.add_update_handler(self._locked_receive)

    def _locked_receive(self, msg):
        self._receive(msg)

    def run(self):
        Thread(target=self._worker, name='Action', args=()).start()
        while True:
            sleep(random() * 3 + 2)
            self._send()

    def _worker(self):
        while True:
            sleep(random() * 3 + 2)
            with self._lock:
                self._action()

    def _send(self):
        with self._lock:
            if len(self._send_queue):
                user, message = self._send_queue.pop(0)
                self._tgClient.send_message(user, message)

    def _find_contact_by_id(self, contact_id):
        for contact in self._dialogs[1]:
            if contact.id == contact_id:
                return contact
        return None

    def _find_contact_by_username(self, username):
        for contact in self._dialogs[1]:
            if (type(contact) is User or type(contact) is Channel) and contact.username == username:
                return contact
        return None

    def _find_contact_by_name(self, title):
        for contact in self._dialogs[1]:
            if type(contact) is User and contact.first_name == title:
                return contact
            elif type(contact) is Channel and contact.title == title:
                return contact
        return None

    def _id_in_list(self, tgid):
        return tgid == self._cwBot.id or \
               tgid == self._captchaBot.id or \
               tgid == self._orderBot.id or \
               tgid == self._tradeBot.id or \
               tgid == self._admin.id or \
               tgid == self._dataBot.id

    def _can_order_id(self, tgid):
        return tgid == self._orderBot.id or \
               tgid == self._admin.id

    def _channel_in_list(self, channel):
        if self._orderGroup:
            return channel.title == self._orderGroup.title
        return False

    def _append_to_send_queue(self, user, message):
        self._send_queue.append([user, message])
