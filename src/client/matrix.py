from PyQt6.QtWidgets import QLabel, QPushButton

from src.client.show_problems import ShowProblems
from src.client.helper_functions import create_widget
from src.client.constants import HIDE, D_HIDE, D_X, BLOCK_SIZE, LINE_WIDTH, LEN_EMER, LEN_NOT_EMER

class Matrix(ShowProblems):
    def __init__(self, main_window, login):
        super().__init__(main_window, login)
        self.setup_local_ui(main_window)

    def setup_local_ui(self, main_window):
        self.text_emer = create_widget(QLabel, "Срочные", self.window)
        self.text_not_emer = create_widget(QLabel, "Не срочные", self.window)
        self.text_imp = create_widget(QLabel, "В\nа\nж\nн\nы\nе", self.window)
        self.text_not_imp = create_widget(QLabel, "Н\nе\nв\nа\nж\nн\nы\nе", self.window)

        self.line1 = create_widget(QLabel, "", main_window)
        self.line1.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')

        self.line2 = create_widget(QLabel, "", main_window)
        self.line2.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')

        self.line3 = create_widget(QLabel, "", main_window)
        self.line3.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')

        self.line4 = create_widget(QLabel, "", main_window)
        self.line4.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')


    def problems_buttons_sector(self, start_x, start_y, width, height, d_y, is_imp, is_emer):
        new_height = start_y
        for i in range(len(self.problems)):
            problem = self.problems[i][0]
            if self.start <= problem.deadline <= self.finish\
                    and problem.is_important == is_imp\
                    and problem.is_emergency == is_emer:
                name_button = create_widget(QPushButton, problem.name, self.window,
                                            start_x, new_height, 2 * width, height, font_size=16)
                name_button.setStyleSheet("color: black;" "border: none;")
                name_button.clicked.connect(self.show_info)
                new_height += height + d_y

                self.buttons_to_index[name_button] = i

    def problems_buttons(self, start_x, start_y, width, height, d_y):
        width -= D_X
        start_with_indent = start_x + 4 * D_X
        for line, x in zip((self.line3, self.line4), (start_with_indent, start_with_indent + 2 * width)):
            line.setGeometry(x, start_y, LINE_WIDTH, 2 * BLOCK_SIZE + height + d_y)

        self.text_emer.setGeometry(start_with_indent + width - LEN_EMER, start_y, 2 * LEN_EMER, height)
        self.text_not_emer.setGeometry(start_with_indent + 3 * width - LEN_NOT_EMER, start_y, 2 * LEN_NOT_EMER, height)
        start_y += height + D_X

        for line in (self.line1, self.line2):
            line.setGeometry(start_x - D_X, start_y, 4 * width + D_X, LINE_WIDTH)
            start_y += BLOCK_SIZE

        start_y -= BLOCK_SIZE
        self.text_imp.setGeometry(start_x, start_y - D_X - BLOCK_SIZE, height, BLOCK_SIZE)
        self.text_not_imp.setGeometry(start_x, start_y - D_X, height, BLOCK_SIZE)
        start_y += d_y

        self.get_problems()
        sector_starts = [(start_with_indent, start_y - BLOCK_SIZE), (start_with_indent + 2 * width, start_y - BLOCK_SIZE),
                         (start_with_indent, start_y), (start_with_indent + 2 * width, start_y)]
        for x, y in sector_starts:
            self.problems_buttons_sector(x, y, width, height, d_y, y != start_y, x == start_with_indent)

    def delete_problems_buttons(self):
        for widget in (self.text_emer, self.text_not_emer, self.text_imp, self.text_not_imp,
                       self.line1, self.line2, self.line3, self.line4):
            widget.setGeometry(HIDE, HIDE, D_HIDE, D_HIDE)
        for button in self.buttons_to_index.keys():
            button.deleteLater()
        self.buttons_to_index.clear()
