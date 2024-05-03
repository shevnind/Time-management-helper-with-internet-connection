from PyQt6.QtGui import QFont

from src.constants import HIDE, D_HIDE

def create_widget(widget_type, text, parent, x=HIDE, y=HIDE, dx=D_HIDE, dy=D_HIDE, font_name="Trebuchet MS", font_size=18):
    widget = widget_type(text, parent)
    widget.setFont(QFont(font_name, font_size))
    widget.setGeometry(x, y, dx, dy)
    widget.show()
    return widget
