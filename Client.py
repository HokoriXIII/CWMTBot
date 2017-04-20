from telethon import TelegramClient, RPCError
from telethon.telegram_client import Session
import config
from Character import Character
from enum import Enum
from multiprocessing import RLock, Lock
from threading import Thread, Timer
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage, UpdatesTg, UpdateNewChannelMessage, \
    UpdateNewMessage, Message
from telethon.tl.functions.contacts import SearchRequest


class CharacterAction(Enum):
    WAIT = 0
    QUEST = 1
    ATTACK = 2
    DEFENCE = 3
    ARENA = 4
    CRAFT = 5
    TRADE = 6
    GET_DATA = 7


client = None


def msg_handler(msg):
    global client
    if type(msg) is UpdatesTg:
        for upd in msg.updates:
            if type(upd) is UpdateNewChannelMessage:
                message = upd.message
                if type(message) is Message:
                    if message.out:
                        print('You sent {} to chat #{}'.format(message.message,
                                                               message.to_id.channel_id))
                    elif client.id_in_list(message.from_id):
                        print('[Chat #{}, user #{} sent {}]'.format(
                            message.to_id.channel_id, message.from_id,
                            message.message))
            elif type(upd) is UpdateNewMessage:
                message = upd.message
                if type(message) is Message:
                    if message.out:
                        print('You sent {} to user #{}'.format(message.message,
                                                               message.to_id.user_id))
                    elif client.id_in_list(message.from_id):
                        print('[User #{} sent {}]'.format(
                            message.from_id,
                            message.message))
    if type(msg) is UpdateShortMessage:
        if msg.out:
            print('You sent {} to user #{}'.format(msg.message,
                                                   msg.user_id))
        elif client.id_in_list(msg.user_id):
            print('[User #{} sent {}]'.format(msg.user_id,
                                              msg.message))

    elif type(msg) is UpdateShortChatMessage:
        if msg.out:
            print('You sent {} to chat #{}'.format(msg.message,
                                                   msg.chat_id))
        elif client.id_in_list(msg.from_id):
            print('[Chat #{}, user #{} sent {}]'.format(
                msg.chat_id, msg.from_id,
                msg.message))


class Client(Thread):
    _phone_lock = Lock()
    _code_lock = Lock()
    _pass_lock = Lock()
    _global_lock = RLock()

    def __init__(self, session):
        super().__init__()
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
        self._cwbot_id = 0
        self._captchabot_id = 0
        self._tradebot_id = 0
        self._admin_id = 0
        self._ordergroup_name = ''
        self._orderbot_id = 0

    def id_in_list(self, tgid):
        self._global_lock.acquire()
        try:
            return tgid == self._cwbot_id or \
                   tgid == self._captchabot_id or \
                   tgid == self._orderbot_id or \
                   tgid == self._tradebot_id or \
                   tgid == self._admin_id
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

    def run(self):
        self._thread_auth()
        self._global_lock.acquire()
        global client
        client = self
        self._cwbot_id = self._tgClient.invoke(SearchRequest(config.CWBot, 1)).results[0].user_id
        self._captchabot_id = self._tgClient.invoke(SearchRequest(config.CaptchaBot, 1)).results[0].user_id
        self._admin_id = self._tgClient.invoke(SearchRequest('@RuckusDJ', 1)).results
        self._tradebot_id = self._tgClient.invoke(SearchRequest(config.TradeBot, 1)).results[0].user_id
        self._orderbot_id = self._tgClient.invoke(SearchRequest('@ToweRobot', 1)).results[0].user_id
        self.handle()
        self._global_lock.release()

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

    def handle(self):
        self._tgClient.add_update_handler(msg_handler)
        # action, action_data = self._character.make_decision()
