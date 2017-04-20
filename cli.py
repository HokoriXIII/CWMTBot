from Client import Client
from telethon import RPCError
from getpass import getpass
import shutil

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
        print_title('Поехали!')

        session = input('Назови сессию (если залогинишься, '
                        'потом не надо будет кучу всего вводить, только это название): ')

        self.client = Client(session)

        print('Взлетаем...')
        self.client.connect()

        if not self.client.authorised():
            phone = input('Нужен телефон: ')
            self.client.code_request(phone)

            code_ok = False

            while not code_ok:
                code = input('Пиши код: ')
                try:
                    code_ok = self.client.login(code)

                # Two-step verification may be enabled
                except RPCError as e:
                    if e.password_required:
                        pw = getpass(
                            'Нужен пароль от двухфакторной авторизации: ')
                        code_ok = self.client.login(password=pw)

        print('Набрали первую космечискую...')
        self.client.start()


if __name__ == '__main__':
    CWCliBot()
