# -*- coding: utf-8 -*-
from telethon.tl.functions.messages import GetInlineBotResultsRequest, SendInlineBotResultRequest
from telethon.utils import get_input_peer
import telethon.helpers as utils
from enums import *
from time import sleep
from random import randint


class Sender:
    def __init__(self, tgClient, cwbot = None, captchabot = None, tradebot = None, orderbot = None, databot = None,
                 admin = None, ordergroup = None):
        self._tgClient = tgClient
        self._cwbot = cwbot
        self._captchabot = captchabot
        self._tradebot = tradebot
        self._orderbot = orderbot
        self._databot = databot
        self._admin = admin
        self._ordergroup = ordergroup

    def send_captcha(self, captcha):
        sleep(randint(8, 20))
        self._tgClient.send_message(self._cwbot, captcha)

    def send_order(self, order):
        if order[0] == CharacterAction.ATTACK:
            result = self._tgClient.invoke(
                GetInlineBotResultsRequest(get_input_peer(self._orderbot),
                                           get_input_peer(self._cwbot),
                                           '', ''))
            res = self._find_inline_by_title(result.results, 'Атака')
            self._tgClient.invoke(
                SendInlineBotResultRequest(get_input_peer(self._cwbot),
                                           utils.generate_random_long(),
                                           result.query_id, res.id))
            sleep(randint(2, 5))
            self._send_castle(order[1])
            sleep(randint(5, 10))
        elif order[0] == CharacterAction.DEFENCE:
            result = self._tgClient.invoke(
                GetInlineBotResultsRequest(get_input_peer(self._orderbot),
                                           get_input_peer(self._cwbot),
                                           '', ''))
            res = self._find_inline_by_title(result.results, 'Защита')
            self._tgClient.invoke(
                SendInlineBotResultRequest(get_input_peer(self._cwbot),
                                           utils.generate_random_long(),
                                           result.query_id, res.id))
            sleep(randint(2, 5))
            self._send_castle(order[1])
            sleep(randint(5, 10))
        elif order[0] == CharacterAction.QUEST:
            self._tgClient.send_message(self._cwbot, Buttons.QUEST.value)
            sleep(randint(2, 5))
            self._tgClient.send_message(self._cwbot, order[1].value)
            sleep(randint(5, 10))
        elif order[0] == CharacterAction.CAPTCHA:
            self._tgClient.send_message(self._captchabot, order[1])
            sleep(28)
        elif order[0] == CharacterAction.GET_DATA:
            self._tgClient.send_message(self._cwbot, order[1].value)
            sleep(randint(5, 10))
        else:
            return

    def _send_castle(self, castle):
        result = self._tgClient.invoke(
            GetInlineBotResultsRequest(get_input_peer(self._orderbot),
                                       get_input_peer(self._cwbot),
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
            SendInlineBotResultRequest(get_input_peer(self._cwbot),
                                       utils.generate_random_long(),
                                       result.query_id, res.id))

    def _find_inline_by_title(self, inline_results, title):
        for res in inline_results:
            if res.title == title:
                return res
