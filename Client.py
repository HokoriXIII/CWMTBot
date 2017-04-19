from telethon import TelegramClient, RPCError
from telethon.telegram_client import Session
import config


class Client:

    def __init__(self, session):
        session = Session.try_load_or_create_new(session)
        session.server_address = '149.154.167.50'
        session.port = 443
        self._tgClient = TelegramClient(session, config.API_ID, config.API_HASH)
        self._phone = ''
        self._code_requested = False
        self._session = session

    def get_session_name(self):
        return self._session

    def connect(self):
        self._tgClient.connect()

    def authorised(self):
        return self._tgClient.is_user_authorized()

    def code_request(self, phone):
        self._phone = phone
        self._tgClient.send_code_request(phone)
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
