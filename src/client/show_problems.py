import datetime
import json

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDateTimeEdit, QLabel, QPushButton

from src.client.add_problem import Problem
from src.client.change_problem import ChangeProblem
from src.client.helper_functions import create_widget
from src.client.constants import HIDE, D_HIDE, START_X, PROBLEM_HEIGHT, WIDTH, PROBLEM_D_Y, LEN1, LEN2, LEN3, LEN4, INDENT
from src.client.client import write_to_server, read_from_server

class ShowProblems():
    def __init__(self, main_window, login):
        self.login = login
        self.change = ChangeProblem(main_window, login)
        self.window = main_window
        self.start = datetime.datetime(datetime.MINYEAR + 1, 1, 1)
        self.finish = datetime.datetime(datetime.MAXYEAR, 12, 31)

        self.setup_ui(main_window)

        self.problems = []
        self.buttons_to_index = {}

        self.get_problems()


    def setup_ui(self, main_window):
        self.title = create_widget(QLabel, "Все задачи", main_window, font_size=24)
        self.text_deadline = create_widget(QLabel, "Дедлайн с", main_window, font_size=16)
        self.text_before = create_widget(QLabel, " по ", main_window, font_size=16)

        self.today_button = create_widget(QPushButton, "Дедлайн сегодня", main_window, font_size=16)
        self.today_button.clicked.connect(self.today)

        self.tomorrow_button = create_widget(QPushButton, "Дедлайн до завтра", main_window, font_size=16)
        self.tomorrow_button.clicked.connect(self.tomorrow)

        self.start_date = QDateTimeEdit(main_window)
        self.start_date.setFont(QFont("Trebuchet MS", 16))
        self.start_date.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)
        self.start_date.setDateTime(self.start)
        self.start_date.show()

        self.finish_date = QDateTimeEdit(main_window)
        self.finish_date.setFont(QFont("Trebuchet MS", 16))
        self.finish_date.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)
        self.finish_date.setDateTime(self.finish)
        self.finish_date.show()

        self.find = create_widget(QPushButton, "Найти", main_window, font_size=16)
        self.find.clicked.connect(self.change_time)

    def change_time(self):
        self.start = self.start_date.dateTime().toPyDateTime()
        self.finish = self.finish_date.dateTime().toPyDateTime()
        self.restart()

    def today(self):
        self.start = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0, 0))
        self.finish = datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59, 59))
        self.restart()

    def tomorrow(self):
        self.start = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0, 0))
        self.finish = datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59, 59))
        self.finish += datetime.timedelta(days=1)
        self.restart()

    def restart(self):
        self.clear()
        self.show()

    def get_problems(self):
        self.problems = []
        write_to_server(f"get problems  {self.login}\n")
        text_problems = str(read_from_server())[:-1]
        if not text_problems:
            return
        print(text_problems)

        list_of_problems = text_problems.split("  ")
        print(list_of_problems, len(list_of_problems))
        for i in range(len(list_of_problems)):
            problem = json.loads(list_of_problems[i], object_hook=Problem)
            self.problems.append((problem, i))
        self.problems.sort()

    def show(self):
        new_height = 2 * PROBLEM_D_Y
        self.title.setGeometry(START_X + INDENT, new_height, 2 * WIDTH, PROBLEM_HEIGHT)
        new_height += PROBLEM_HEIGHT + 2 * PROBLEM_D_Y

        self.today_button.setGeometry(START_X, new_height, 2 * WIDTH, PROBLEM_HEIGHT)
        self.tomorrow_button.setGeometry(START_X + 2 * WIDTH, new_height, 2 * WIDTH, PROBLEM_HEIGHT)
        new_height += PROBLEM_HEIGHT + PROBLEM_D_Y

        self.text_deadline.setGeometry(START_X, new_height, LEN1, PROBLEM_HEIGHT)
        self.start_date.setGeometry(START_X + LEN1, new_height, LEN2, PROBLEM_HEIGHT)
        self.text_before.setGeometry(START_X + LEN1 + LEN2, new_height, LEN3, PROBLEM_HEIGHT)
        self.finish_date.setGeometry(START_X + LEN1 + LEN2 + LEN3, new_height, LEN2, PROBLEM_HEIGHT)
        self.find.setGeometry(START_X + LEN1 + 2 * LEN2 + LEN3, new_height, LEN4, PROBLEM_HEIGHT)
        new_height += PROBLEM_HEIGHT + 2 * PROBLEM_D_Y
        self.problems_buttons(START_X, new_height, WIDTH, PROBLEM_HEIGHT, PROBLEM_D_Y)

    def problems_buttons(self, START_X, new_height, WIDTH, PROBLEM_HEIGHT, PROBLEM_D_Y):
        raise NotImplementedError()

    def hide_buttons(self):
        for widget in (self.title, self.today_button, self.tomorrow_button, self.text_deadline, self.start_date,
                       self.text_before, self.finish_date, self.find):
            widget.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)
        self.change.hide_all_buttons()

    def delete_problems_buttons(self):
        raise NotImplementedError()

    def clear(self):
        self.hide_buttons()
        self.delete_problems_buttons()

    def show_info(self):
        button = QApplication.instance().sender()
        index = self.buttons_to_index[button]
        self.clear()
        self.change.show_problem(self.problems[index][1], self.problems[index][0])
