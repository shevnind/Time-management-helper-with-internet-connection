import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from src.login_registration import RegistrationOrLogin
from src.add_problem import AddProblem
from src.helper_functions import create_widget
from src.matrix import Matrix
from src.print_by_dates import List
from src.constants import WINDOW_SIZE_X, WINDOW_SIZE_Y, MAIN_START_X, MAIN_START_Y, MAIN_WIDTH
from src.constants import MAIN_HEIGHT, LINE_X, LINE_Y, LINE_WIDTH
from src.client import connect

login = "admin"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        connect()

        self.setup_ui()
        self.log_reg = RegistrationOrLogin(self)

    def setup_ui(self):
        self.setWindowTitle("Time-management helper")
        self.setFixedSize(WINDOW_SIZE_X, WINDOW_SIZE_Y)

        self.add_problem_button = create_widget(QPushButton, "Добавить задачу", self)
        self.add_problem_button.clicked.connect(self.add_problem)

        self.list_button = create_widget(QPushButton, "Список задач", self)
        self.list_button.clicked.connect(self.show_list)

        self.matrix_button = create_widget(QPushButton, "Матрица Эйзенхауэра", self)
        self.matrix_button.clicked.connect(self.show_matrix)

        self.line = create_widget(QLabel, "", self)
        self.line.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')

    def show_main_buttons(self):
        curr_y = MAIN_START_Y
        for widget in [self.add_problem_button, self.list_button, self.matrix_button]:
            widget.setGeometry(MAIN_START_X, curr_y, MAIN_WIDTH, MAIN_HEIGHT)
            curr_y += MAIN_START_Y + MAIN_HEIGHT
        self.line.setGeometry(LINE_X, LINE_Y, LINE_WIDTH, WINDOW_SIZE_Y)

    def start(self, new_login):
        global login
        login = new_login
        self.show_main_buttons()
        self.add = AddProblem(self, login)
        self.list = List(self, login)
        self.matrix = Matrix(self, login)

    def add_problem(self):
        self.hide_all_buttons()
        self.add.show()

    def show_matrix(self):
        self.hide_all_buttons()
        self.matrix.show()

    def show_list(self):
        self.hide_all_buttons()
        self.list.show()

    def hide_all_buttons(self):
        self.add.hide_buttons()
        self.list.clear()
        self.matrix.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
