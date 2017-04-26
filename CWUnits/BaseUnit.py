from abc import ABCMeta, abstractmethod
from telethon import TelegramClient
from Character import Character
from telethon.tl.types import User, Channel, Chat
import config
from multiprocessing import RLock
from time import sleep
from threading import Thread, Timer
from random import randint


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
        self._captchaBot = self._find_contact_by_username(config.CaptchaBot)
        self._tradeBot = self._find_contact_by_username(config.TradeBot)
        self._orderBot = self._find_contact_by_username(self._character.config.orderBot)
        self._dataBot = self._find_contact_by_username(self._character.config.dataBot)
        self._admin = self._find_contact_by_username(self._character.config.admin)
        self._orderGroup = self._find_contact_by_name(self._character.config.orderChat)
        if not self._admin:
            # Если юзера-админа не нашли, то админим сами
            self._admin = self._tgClient.session.user
        self._tgClient.add_update_handler(self._receive)

    def run(self):
        Timer(1, self._worker).start()
        while True:
            self._send()
            sleep(0.1)

    def _worker(self):
        self._action()
        Timer(randint(5, 7), self._worker).start()

    def _send(self):
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
            if type(contact) is not Chat and contact.username == username:
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
        return channel.title == self._orderGroup.title

    def _append_to_send_queue(self, user, message):
        self._send_queue.append([user, message])
