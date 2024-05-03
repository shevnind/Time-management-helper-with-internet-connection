import datetime
import json

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QDateTimeEdit, QLabel, QLineEdit, QPushButton, QTextEdit

from src.helper_functions import create_widget
from src.client import write_to_server, read_from_server
from src.constants import HIDE, D_HIDE, START_X, TEXT_START_Y, WIDTH, TEXT_HEIGHT, TEXT_D_Y, INDENT


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return obj


class Problem:
    def __init__(self, dict):
        self.name = ""
        self.description = ""
        self.is_important = False
        self.is_emergency = False
        self.deadline = datetime.datetime.now()
        self.tags = list()
        vars(self).update(dict)
        self.deadline = datetime.datetime.fromisoformat(str(self.deadline))

    def clear(self):
        self.name = ""
        self.description = ""
        self.is_important = False
        self.is_emergency = False
        self.deadline = datetime.datetime.now()
        self.tags = []

    def __lt__(self, other):
        if self.deadline.date() != other.deadline.date():
            return self.deadline.date() < other.deadline.date()
        if self.is_important != other.is_important:
            return self.is_important > other.is_important
        if self.is_emergency != other.is_emergency:
            return self.is_emergency > other.is_emergency
        return self.name < other.name


class AddProblem():
    def __init__(self, main_window, login):
        self.login = login
        self.setup_ui(main_window)
        self.new_problem = Problem({})

    def setup_ui(self, main_window):
        self.title = create_widget(QLabel, "Новая задача", main_window, font_size=24)
        self.text_name = create_widget(QLabel, "Имя задачи:", main_window)
        self.name = create_widget(QLineEdit, "", main_window)
        self.text_desc = create_widget(QLabel, "Описание:", main_window)
        self.desc = create_widget(QTextEdit, "", main_window)
        self.text_deadline = create_widget(QLabel, "Дедлайн:", main_window)
        self.text_tag = create_widget(QLabel, "Тег:", main_window)
        self.tag = create_widget(QLineEdit, "", main_window)

        self.deadline = QDateTimeEdit(main_window)
        self.deadline.setFont(QFont("Trebuchet MS", 18))
        self.deadline.setDateTime(datetime.datetime.now())
        self.deadline.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)
        self.deadline.show()

        self.imp = create_widget(QCheckBox, "Важная задача", main_window)
        self.imp.toggled.connect(self.change_importance)

        self.emer = create_widget(QCheckBox, "Срочная задача", main_window)
        self.emer.toggled.connect(self.change_emergency)

        self.save_tag = create_widget(QPushButton, "Добавить тег", main_window)
        self.save_tag.clicked.connect(self.add_tag)

        self.save_problem = create_widget(QPushButton, "Сохранить задачу", main_window, font_size=24)
        self.save_problem.clicked.connect(self.save)

    def show(self):
        new_height = TEXT_START_Y
        self.title.setGeometry(START_X + INDENT, new_height, 2 * WIDTH, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT + 3 * TEXT_D_Y

        self.text_name.setGeometry(START_X, new_height, WIDTH, TEXT_HEIGHT)
        self.name.setGeometry(START_X + WIDTH, new_height, 3 * WIDTH, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT + TEXT_D_Y

        self.text_desc.setGeometry(START_X, new_height, WIDTH, TEXT_HEIGHT)
        self.desc.setGeometry(START_X + WIDTH, new_height, 3 * WIDTH, 5 * TEXT_HEIGHT)
        new_height += 5 * TEXT_HEIGHT + TEXT_D_Y

        self.text_deadline.setGeometry(START_X, new_height, WIDTH, TEXT_HEIGHT)
        self.deadline.setGeometry(START_X + WIDTH, new_height, 3 * WIDTH, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT + TEXT_D_Y

        self.imp.setGeometry(START_X + WIDTH + 2 * TEXT_D_Y, new_height, 2 * WIDTH, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT + TEXT_D_Y

        self.emer.setGeometry(START_X + WIDTH + 2 * TEXT_D_Y, new_height, 2 * WIDTH, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT + TEXT_D_Y

        self.text_tag.setGeometry(START_X, new_height, WIDTH, TEXT_HEIGHT)
        self.tag.setGeometry(START_X + WIDTH, new_height, 3 * WIDTH, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT

        self.save_tag.setGeometry(START_X + 3 * WIDTH - TEXT_HEIGHT, new_height,
                                  WIDTH + TEXT_HEIGHT, TEXT_HEIGHT)
        new_height += TEXT_HEIGHT + 2 * TEXT_D_Y

        self.save_problem.setGeometry(START_X + WIDTH, new_height, 2 * WIDTH, 2 * TEXT_HEIGHT)

    def change_importance(self, cond):
        self.new_problem.is_important = cond

    def change_emergency(self, cond):
        self.new_problem.is_emergency = cond

    def add_tag(self):
        new_tag = self.tag.text()
        if not new_tag in self.new_problem.tags:
            self.new_problem.tags.append(new_tag)
        self.tag.setText("")

    def save(self):
        self.new_problem.name = self.name.text()
        self.new_problem.description = self.desc.toPlainText()
        self.new_problem.deadline = self.deadline.dateTime().toPyDateTime()

        if self.new_problem.name != "":
            write_to_server("add problem  " + self.login + "  " +
                            json.dumps(self.new_problem.__dict__, cls=DateTimeEncoder) + '\n')
            print(read_from_server())
            self.clear()
            self.hide_buttons()

    def clear(self):
        self.name.setText("")
        self.desc.setText("")
        self.deadline.setDateTime(datetime.datetime.now())
        self.imp.setChecked(False)
        self.emer.setChecked(False)
        self.tag.setText("")
        self.new_problem.clear()

    def hide_buttons(self):
        for widget in (self.title, self.text_name, self.name, self.text_desc, self.desc, self.text_deadline,
                       self.deadline, self.imp, self.emer, self.text_tag, self.tag, self.save_tag, self.save_problem):
            widget.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)
