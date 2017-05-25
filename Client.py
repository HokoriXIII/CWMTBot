# -*- coding: utf-8 -*-
import importlib
from telethon import TelegramClient, RPCError
from telethon.telegram_client import Session
import config
from Character import Character
from multiprocessing import RLock, Lock
from threading import Thread


class Client(Thread):
    _phone_lock = Lock()
    _code_lock = Lock()
    _pass_lock = Lock()

    def __init__(self, session):
        super().__init__()
        self._global_lock = RLock()
        self._character = Character(session)
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
        self._worker = None
        self._module = None

    def set_phone(self, phone):
        self._phone = phone
        self._phone_lock.release()

    def set_code(self, code):
        self._code = code
        self._code_lock.release()

    def set_pass(self, password):
        self._pass = password
        self._pass_lock.release()

    def set_opts(self, opts):
        self._character.set_opts(opts)

    def run(self):
        self._thread_auth()
        if self._character.config.module:
            self._module = importlib.import_module('CWUnits.' + self._character.config.module)
            self._worker = self._module.Module(self._tgClient, self._character)
            self._worker.setName('Sender')
            self._worker.start()

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
                self._global_lock.acquire()
                self.login(self._code)
                self._code_lock.release()
                self._global_lock.release()
            except RPCError as e:
                if e.password_required:
                    self._need_pass = True
                    self._code_lock.release()
                    self._global_lock.acquire()
                    self._pass_lock.acquire()
                    self.login(password=self._pass)
                    self._global_lock.release()

    def pass_needed(self):
        self._code_lock.acquire()
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
