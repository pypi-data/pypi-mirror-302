from types import ModuleType
import importlib

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QLayout

from src.PyQtPath.types import QObjectSubClass


def child(top_object: QObject, path: str) -> QObjectSubClass:
    if top_object is None:
        return None
    if path is None or len(path) == 0:
        return top_object
    normalized_path: list[(type[QObject], int)] = __normalize_path(path)
    return __nested_child(top_object, normalized_path)


def __nested_child(top_object: QObject, path: list[(type[QObject], int)]) -> QObjectSubClass:
    current_object: QObject = top_object
    for part in path:
        clazz: type[QObject] = part[0]
        index: int = part[1]
        if isinstance(current_object, QLayout):
            if issubclass(clazz, QLayout):
                children: list[QObject] = current_object.findChildren(clazz)
            else:
                children: list[QObject] = __get_layout_children(current_object)
        else:
            if issubclass(clazz, QLayout):
                children: list[QObject] = current_object.findChildren(clazz)
            else:
                children: list[QObject] = current_object.findChildren(clazz)
        if len(children) == 0:
            return None
        current_object = children[index]
    return current_object


def __normalize_path(path: str) -> list[(type[QObject], int)]:
    if path is None or len(path) == 0:
        return []
    parts: list[str] = path.split("/")
    for i, part in enumerate(parts):
        if part.isdigit():
            continue
        next_part: str = parts[i + 1] if i < len(parts) - 1 else None
        module: ModuleType = importlib.import_module("PyQt6.QtWidgets")
        clazz: type[QObject] = getattr(module, part)
        if next_part is not None and next_part.isdigit():
            yield clazz, int(next_part)
        else:
            yield clazz, 0


def __get_layout_children(layout: QLayout) -> list[QObject]:
    children: list[QObject] = []
    for i in range(layout.count()):
        children.append(layout.itemAt(i).widget())
    return children
