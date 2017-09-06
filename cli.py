# -*- coding: utf-8 -*-
from time import sleep

from Client import Client
from getpass import getpass
from getopt import getopt
import shutil
import sys

# Get the (current) number of lines in the terminal
cols, rows = shutil.get_terminal_size()


def print_title(title):
    # Clear previous window
    print('\n')
    available_cols = cols - 2  # -2 since we omit '┌' and '┐'
    print('┌{}┐'.format('─' * available_cols))
    print('│{}│'.format(title.center(available_cols)))
    print('└{}┘'.format('─' * available_cols))


class CWCliBot:

    def __init__(self):
        opts, args = getopt(sys.argv[1:], 'm:a:o:c:d:s:', ['module=', 'admin=', 'order=', 'chat=', 'data=', 'session='])
        print_title('Поехали!')
        session = ''
        for opt, arg in opts:
            if opt in ('-s', '--session'):
                session = arg
        if session == '':
            session = input('Назови сессию (если залогинишься, '
                            'потом не надо будет кучу всего вводить, только это название): ')

        self.client = Client(session)
        self.client.set_opts(opts)
        self.client.setName(session)

        self.client.start()
        sleep(1)
        print('Взлетаем...')

        if not self.client.authorised():
            phone = input('Нужен телефон: ')
            self.client.set_phone(phone)

            code_ok = False

            while not code_ok:
                code = input('Пиши код: ')
                self.client.set_code(code)
                if self.client.pass_needed():
                    pw = input(
                        'Нужен пароль от двухфакторной авторизации: ')
                    self.client.set_pass(pw)
                if self.client.authorised():
                    code_ok = True

        print('Набрали первую космечискую...')


if __name__ == '__main__':
    CWCliBot()
