from PyQt6.QtWidgets import QPushButton

from src.add_problem import AddProblem
from src.helper_functions import create_widget
from src.constants import HIDE, D_HIDE, START_X, LAST_Y, TEXT_HEIGHT, WIDTH
from src.client import write_to_server, read_from_server

class ChangeProblem(AddProblem):
    def __init__(self, main_window, login):
        super().__init__(main_window, login)

        self.done = create_widget(QPushButton, "Сделано!", main_window, font_size=24)
        self.done.clicked.connect(self.mark_as_done)

        self.index = -1
        self.hide_all_buttons()

    def erase_problem(self):
        write_to_server("delete problem  " + self.login + "  " + str(self.index) + '\n')
        print(read_from_server())
    def mark_as_done(self):
        self.erase_problem()
        self.hide_all_buttons()

    def show_problem(self, index, problem):
        self.new_problem = problem
        self.index = index
        self.show()
        self.title.setText("Изменить задачу")
        self.name.setText(problem.name)
        self.desc.setText(problem.description)
        self.deadline.setDateTime(problem.deadline)
        if problem.is_important:
            self.imp.setChecked(True)
        if problem.is_emergency:
            self.emer.setChecked(True)
        self.save_problem.setText("Сохранить")
        self.save_problem.setGeometry(START_X, LAST_Y, 2 * WIDTH, 2 * TEXT_HEIGHT)
        self.save_problem.clicked.disconnect()
        self.save_problem.clicked.connect(self.save_changes)
        self.done.setGeometry(START_X + 2 * WIDTH, LAST_Y, 2 * WIDTH, 2 * TEXT_HEIGHT)

    def hide_all_buttons(self):
        self.hide_buttons()
        self.done.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)

    def save_changes(self):
        self.erase_problem()
        self.save()
        self.hide_all_buttons()
