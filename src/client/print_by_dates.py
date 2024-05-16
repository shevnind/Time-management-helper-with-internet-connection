import datetime

from PyQt6.QtWidgets import QLabel, QPushButton

from src.client.show_problems import ShowProblems
from src.client.helper_functions import create_widget

class List(ShowProblems):
    def __init__(self, main_window, login):
        super().__init__(main_window, login)
        self.dates = []

    def problems_buttons(self, start_x, new_height, width, height, d_y):
        self.get_problems()
        cur_date = (self.start - datetime.timedelta(days=1)).date()
        for i in range(len(self.problems)):
            problem = self.problems[i][0]
            if self.start <= problem.deadline <= self.finish:
                if problem.deadline.date() != cur_date:
                    cur_date = problem.deadline.date()
                    text = create_widget(QLabel, str(cur_date) + ":", self.window,
                                         start_x, new_height, width, height, font_size=16)
                    self.dates.append(text)

                name_button = create_widget(QPushButton, problem.name, self.window,
                                            start_x + width, new_height, 3 * width, height, font_size=16)
                color = "red" if problem.is_important else "green"
                name_button.setStyleSheet("color: " + color + ";" "border: none;")
                name_button.clicked.connect(self.show_info)
                new_height += height + d_y

                self.buttons_to_index[name_button] = i

    def delete_problems_buttons(self):
        for text in self.dates:
            text.deleteLater()
        self.dates.clear()
        for button in self.buttons_to_index.keys():
            button.deleteLater()
        self.buttons_to_index.clear()
