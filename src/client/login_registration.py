from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton

from src.client.helper_functions import create_widget
from src.client.constants import HIDE, D_HIDE, TEXT_HEIGHT, TEXT_D_Y, LOGIN_WIDTH, D_X, ALL_LEN, WRONG_START_Y, \
                            LOGIN_START_Y, LOGIN_START_X, LOGIN_BUTTON_LEN, REGISTRATION_BUTTON_LEN, OR_LEN, \
                            WRONG_LOGIN_START_Y, WRONG_PASSWORD_START_Y, MAIN_START_Y, MAIN_START_X
from src.client.client import write_to_server, read_from_server

class RegistrationOrLogin():
    def __init__(self, main_window):
        self.window = main_window
        self.setup_ui()
        self.show_main_text()

    def setup_ui(self):
        self.to_login_button = create_widget(QPushButton, "Войдите", self.window, font_size=24)
        self.to_login_button.setStyleSheet("color: blue;" "border: none;")
        self.to_login_button.clicked.connect(self.show_login)

        self.or_text = create_widget(QLabel, " или ", self.window, font_size=24)

        self.to_registration_button = create_widget(QPushButton, "зарегистрируйтесь", self.window, font_size=24)
        self.to_registration_button.setStyleSheet("color: blue;" "border: none;")
        self.to_registration_button.clicked.connect(self.show_registration)

        self.text = create_widget(QLabel, "чтобы воспользоваться сервисом", self.window, font_size=24)

        self.autorisation_title = create_widget(QLabel, "Вход", self.window, font_size=24)
        self.login_text = create_widget(QLabel, "Ваш логин:", self.window, font_size=24)
        self.password_text = create_widget(QLabel, "Ваш пароль:", self.window, font_size=24)
        self.login = create_widget(QLineEdit, "", self.window)
        self.password = create_widget(QLineEdit, "", self.window)

        self.autorisation_button = create_widget(QPushButton, "", self.window, font_size=24)
        self.autorisation_button.clicked.connect(self.login_or_registration)

        self.back_button = create_widget(QPushButton, "Назад", self.window, font_size=16)
        self.back_button.clicked.connect(self.show_main_text)

        self.error_text = create_widget(QLabel, "", self.window, font_size=14)
        self.error_text.setStyleSheet("color: red;" "border: none;")

    def hide_buttons(self):
        for widget in [self.to_login_button, self.to_registration_button, self.or_text, self.text,
                       self.autorisation_title, self.login_text, self.password_text, self.login,
                       self.password, self.autorisation_button, self.error_text, self.back_button]:
            widget.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)

    def show_main_text(self):
        self.hide_buttons()
        curr_y = LOGIN_START_Y
        curr_x = LOGIN_START_X
        for widget, len in zip([self.to_login_button, self.or_text, self.to_registration_button],
                               [LOGIN_BUTTON_LEN, OR_LEN, REGISTRATION_BUTTON_LEN]):
            widget.setGeometry(curr_x, curr_y, len, TEXT_HEIGHT)
            curr_x += len
        curr_y += TEXT_HEIGHT + TEXT_D_Y
        self.text.setGeometry(LOGIN_START_X + 2 * D_X, curr_y, ALL_LEN, TEXT_HEIGHT)

    def show_login_or_registration(self):
        self.hide_buttons()
        curr_y = LOGIN_START_Y
        self.autorisation_title.setGeometry(LOGIN_START_X + 2 * LOGIN_WIDTH, curr_y, 2 * LOGIN_WIDTH, TEXT_HEIGHT)
        curr_y += TEXT_HEIGHT + 2 * TEXT_D_Y

        for widget, start_x, width in zip([self.login_text, self.login], [LOGIN_START_X, LOGIN_START_X + 2 * LOGIN_WIDTH],
                                          [2 * LOGIN_WIDTH, 4 * LOGIN_WIDTH]):
            widget.setGeometry(start_x, curr_y, width, TEXT_HEIGHT)
        curr_y += TEXT_HEIGHT + 2 * TEXT_D_Y

        for widget, start_x, width in zip([self.password_text, self.password], [LOGIN_START_X, LOGIN_START_X + 2 * LOGIN_WIDTH],
                                          [2 * LOGIN_WIDTH, 4 * LOGIN_WIDTH]):
            widget.setGeometry(start_x, curr_y, width, TEXT_HEIGHT)
        curr_y += TEXT_HEIGHT + 2 * TEXT_D_Y

        self.back_button.setGeometry(MAIN_START_X, MAIN_START_Y, LOGIN_WIDTH, TEXT_HEIGHT)
        self.autorisation_button.setGeometry(LOGIN_START_X + LOGIN_WIDTH, curr_y, 4 * LOGIN_WIDTH, 2 * TEXT_HEIGHT)

    def show_registration(self):
        self.autorisation_title.setText("Регистрация")
        self.autorisation_button.setText("Зарегистрироваться")
        self.show_login_or_registration()

    def show_login(self):
        self.autorisation_title.setText("Вход")
        self.autorisation_button.setText("Войти")
        self.show_login_or_registration()

    def login_or_registration(self):
        if self.autorisation_title.text() == "" or self.login.text() == "":
            return
        message = "login  " if self.autorisation_title.text() == "Вход" else "register  "
        login = self.login.text()
        message += f"{login}  {self.password.text()}\n"
        write_to_server(message)
        helper = read_from_server()
        message = helper[:-1]
        print(message)
        if message == "success":
            self.hide_buttons()
            self.window.start(login)
        else:
            self.error_text.setGeometry(LOGIN_START_X + 2 * LOGIN_WIDTH, WRONG_LOGIN_START_Y, 4 * LOGIN_WIDTH, TEXT_HEIGHT)
            if message == "login is busy":
                self.error_text.setText("Такой логин уже занят")
            elif message == "wrong login":
                self.error_text.setText("Неправильный логин")
            elif message == "wrong password":
                self.error_text.setText("Неправильный пароль")
                self.error_text.setGeometry(LOGIN_START_X + 2 * LOGIN_WIDTH, WRONG_PASSWORD_START_Y,
                                       4 * LOGIN_WIDTH, TEXT_HEIGHT)
            else:
                self.error_text.setText("Ошибка при подключении к серверу")
                self.error_text.setGeometry(LOGIN_START_X + 2 * LOGIN_WIDTH, WRONG_START_Y,
                                       4 * LOGIN_WIDTH, TEXT_HEIGHT)

