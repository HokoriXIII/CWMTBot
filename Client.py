# -*- coding: utf-8 -*-
import importlib
from telethon import TelegramClient, RPCError
from telethon.telegram_client import Session
import config
from Character import Character, Castle
from multiprocessing import RLock, Lock
from threading import Thread, Timer
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage, UpdatesTg, UpdateNewChannelMessage, \
    UpdateNewMessage, Message, User, Channel
from telethon.tl.functions.messages import GetInlineBotResultsRequest, SendInlineBotResultRequest
from telethon.utils import get_input_peer
import telethon.helpers as utils
from time import sleep
import random
import pytz
from pytz import timezone
from datetime import datetime, timedelta, time
import re
import regexp


class Client(Thread):
    _phone_lock = Lock()
    _code_lock = Lock()
    _pass_lock = Lock()
    _global_lock = RLock()
    _battle_hours = [0, 4, 8, 12, 16, 20]
    _sleep_intervals = [(time(0, 10), time(3, 50)),
                        (time(4, 15), time(7, 45))]

    def __init__(self, session):
        super().__init__()
        self.character = Character(session)
        self._session = session
        self._phone = ''
        self._code = ''
        self._pass = ''
        self._tgClient = None
        self._code_requested = False
        self._session = session
        self._phone_lock.acquire()
        self._pass_lock.acquire()
        self._code_lock.acquire()
        self._need_pass = False
        self._cwbot = None
        self._captchabot = None
        self._tradebot = None
        self._admin = None
        self._ordergroup = None
        self._orderbot = None
        self._databot = None
        self._dialogs = None
        self._timezone = timezone('Europe/Moscow')
        self._sender = None
        self._sender_module = None

    def id_in_list(self, tgid):
        self._global_lock.acquire()
        try:
            return tgid == self._cwbot.id or \
                   tgid == self._captchabot.id or \
                   tgid == self._orderbot.id or \
                   tgid == self._tradebot.id or \
                   tgid == self._admin.id or \
                   tgid == self._databot.id
        finally:
            self._global_lock.release()

    def can_order_id(self, tgid):
        self._global_lock.acquire()
        try:
            return tgid == self._orderbot.id or \
                   tgid == self._admin.id or \
                   tgid == self._databot.id
        finally:
            self._global_lock.release()

    def channel_in_list(self, channel):
        self._global_lock.acquire()
        try:
            return channel.title == self._ordergroup.title
        finally:
            self._global_lock.release()

    def set_phone(self, phone):
        self._phone = phone
        self._phone_lock.release()

    def set_code(self, code):
        self._code = code
        self._code_lock.release()

    def set_pass(self, password):
        self._pass = password
        self._pass_lock.release()

    def find_contact_by_id(self, contact_id):
        for contact in self._dialogs[1]:
            if contact.id == contact_id:
                return contact
        return None

    def find_contact_by_username(self, username):
        for contact in self._dialogs[1]:
            if contact.username == username:
                return contact
        return None

    def find_contact_by_name(self, title):
        for contact in self._dialogs[1]:
            if type(contact) is User and contact.first_name == title:
                return contact
            elif type(contact) is Channel and contact.title == title:
                return contact
        return None

    def run(self):
        self._thread_auth()
        self._global_lock.acquire()
        self._dialogs = self._tgClient.get_dialogs(1000)
        if self.character.config.module:
            self._sender_module = importlib.import_module(self.character.config.module)
        self._cwbot = self.find_contact_by_username(config.CWBot)
        self._captchabot = self.find_contact_by_username(config.CaptchaBot)
        self._tradebot = self.find_contact_by_username(config.TradeBot)
        self._orderbot = self.find_contact_by_username(self.character.config.orderBot)
        self._databot = self.find_contact_by_username(self.character.config.dataBot)
        self._admin = self.find_contact_by_username(self.character.config.admin)
        self._ordergroup = self.find_contact_by_name(self.character.config.orderChat)
        if not self._admin:
            # Если юзера-админа не нашли, то админим сами
            self._admin = self._tgClient.session.user
        if self._sender_module:
            self._sender = self._sender_module.Sender(self._tgClient, cwbot=self._cwbot, captchabot=self._captchabot,
                                                      tradebot=self._tradebot, orderbot=self._orderbot,
                                                      databot=self._databot, admin=self._admin,
                                                      ordergroup=self._ordergroup)
        self.handle()
        self._global_lock.release()

        while True:
            if self._sender:
                self._sender.send_order(self.character.ask_action())
            sleep(random.randint(2, 5))

    def _thread_auth(self):
        self._global_lock.acquire()
        session = Session.try_load_or_create_new(self._session)
        session.server_address = '149.154.167.50'
        session.port = 443
        self._tgClient = TelegramClient(session, config.API_ID, config.API_HASH)
        self.connect()
        self._global_lock.release()
        while not self.authorised():
            self._phone_lock.acquire()
            self.code_request()
            self._code_lock.acquire()
            try:
                self.login(self._code)
            except RPCError as e:
                if e.password_required:
                    self._need_pass = True
                    self._pass_lock.acquire()
                    self.login(password=self._pass)

    def pass_needed(self):
        return self._need_pass

    def get_session_name(self):
        return self._session

    def connect(self):
        self._tgClient.connect()

    def authorised(self):
        self._global_lock.acquire()
        try:
            return self._tgClient.is_user_authorized() if self._tgClient else False
        finally:
            self._global_lock.release()

    def code_request(self):
        self._tgClient.send_code_request(self._phone)
        self._code_requested = True

    def login(self, code=None, password=None):
        try:
            if self._phone and self._code_requested:
                if password:
                    res = self._tgClient.sign_in(password=password)
                    return res
                res = self._tgClient.sign_in(self._phone, code)
                return res
            return 0
        except RPCError as e:
            raise e

    def msg_handler(self, msg):
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
                            if channel and self.channel_in_list(channel):
                                if self.can_order_id(message.from_id):
                                    self.character.set_order(message.message)
                elif type(upd) is UpdateNewMessage:
                    message = upd.message
                    if type(message) is Message:
                        if message.out:
                            if message.to_id.user_id == message.from_id:
                                self.character.set_order(message.message)
                        elif self.id_in_list(message.from_id):
                            if message.from_id == self.can_order_id(message.from_id):
                                print('Получли приказ')
                                self.character.set_order(message.message)
                            elif message.from_id == self._cwbot.id:
                                print('Получили сообщение от ChatWars')
                                self.character.parse_message(message.message)
        elif type(msg) is UpdateShortMessage:
            if msg.out:
                print('You sent {} to user #{}'.format(msg.message,
                                                       msg.user_id))
            elif self.id_in_list(msg.user_id):
                print('[User #{} sent {}]'.format(msg.user_id,
                                                  msg.message))

        elif type(msg) is UpdateShortChatMessage:
            if msg.out:
                print('You sent {} to chat #{}'.format(msg.message,
                                                       msg.chat_id))
            elif self.id_in_list(msg.from_id):
                print('[Chat #{}, user #{} sent {}]'.format(
                    msg.chat_id, msg.from_id,
                    msg.message))

    def handle(self):
        self._tgClient.add_update_handler(self.msg_handler)
        # action, action_data = self._character.make_decision()
