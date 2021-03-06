# -*- coding: utf-8 -*-
import importlib
import platform

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.session import Session
import config
from Character import Character
from multiprocessing import RLock, Lock, Event
from threading import Thread


class Client(Thread):
    _phone_lock = Lock()
    _code_lock = Lock()
    _pass_lock = Lock()
    event_pass = Event()

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
        self.event_pass.clear()

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
        with self._global_lock:
            session = Session.try_load_or_create_new(self._session)
            session.server_address = '149.154.167.50'
            session.port = 443
            session.device_model = platform.node()
            session.system_version = platform.system()
            session.app_version = TelegramClient.__version__
            session.lang_code = 'en'
            self._tgClient = TelegramClient(session, config.API_ID, config.API_HASH)
            self.connect()
        while not self.authorised():
            self._phone_lock.acquire()
            self.code_request()
            self._global_lock.acquire()
            self._code_lock.acquire()
            try:
                self.login(self._code)
                self._code_lock.release()
                self.event_pass.set()
            except SessionPasswordNeededError:
                self._need_pass = True
                self.event_pass.set()
                self._pass_lock.acquire()
                self.login(password=self._pass)
            finally:
                self._global_lock.release()

    def pass_needed(self):
        self.event_pass.wait()
        self.event_pass.clear()
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
        except SessionPasswordNeededError as e:
            raise e
