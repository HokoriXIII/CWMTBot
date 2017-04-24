# -*- coding: utf-8 -*-
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
        opts, args = getopt(sys.argv[1:], 'm:a:o:c:d:', ['module=', 'admin=', 'order=', 'chat=', 'data='])
        print_title('Поехали!')

        session = input('Назови сессию (если залогинишься, '
                        'потом не надо будет кучу всего вводить, только это название): ')

        self.client = Client(session)
        self.client.set_opts(opts)
        self.client.setName(session)

        self.client.start()

        print('Взлетаем...')

        if not self.client.authorised():
            phone = input('Нужен телефон: ')
            self.client.set_phone(phone)

            code_ok = False

            while not code_ok:
                code = input('Пиши код: ')
                self.client.set_code(code)
                if self.client.pass_needed():
                    pw = getpass(
                        'Нужен пароль от двухфакторной авторизации: ')
                    self.client.set_pass(pw)
                    if self.client.authorised():
                        code_ok = True

        print('Набрали первую космечискую...')


if __name__ == '__main__':
    CWCliBot()
