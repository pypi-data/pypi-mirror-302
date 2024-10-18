from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QCheckBox, QLabel, QDialog, QPushButton, QTableWidget, QGroupBox


def path(widget: QObject):
    return Path([widget])


class Path:
    def __init__(self, objects: list[QObject]) -> None:
        self.widgets: list[QObject] = objects

    def get(self, index: int = 0) -> QObject:
        return self.widgets[index]

    def checkbox(self, index: int = 0) -> 'Path':
        return self.child(QCheckBox, index)

    def label(self, index: int = 0) -> 'Path':
        return self.child(QLabel, index)

    def dialog(self, index: int = 0) -> 'Path':
        return self.child(QDialog, index)

    def button(self, index: int = 0) -> 'Path':
        return self.child(QPushButton, index)

    def table(self, index: int = 0) -> 'Path':
        return self.child(QTableWidget, index)

    def group(self, index: int = 0) -> 'Path':
        return self.child(QGroupBox, index)

    def child(self, clazz: type[QObject], index: int = 0):
        return Path([self.widgets[0].findChildren(clazz)[index]])
