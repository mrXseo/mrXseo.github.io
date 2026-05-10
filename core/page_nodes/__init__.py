from typing import List, Tuple, Optional
from ..page_elements import PageElement, ElementTag, Html

class SiteNode:
    """
    Декларативный узел дерева страницы.
    Хранит метаданные, элемент и дочерние узлы.
    Управляет жизненным циклом PageElement: init → ready → build → get_result.
    """
    def __init__(self, name: str, elem: Optional[PageElement] = None, meta: dict = None):
        self.name = name
        self.elem = elem
        self.children: List['SiteNode'] = []
        self.meta = meta or {}
        self.tag = ""

    def add_child(self, node: 'SiteNode'):
        self.children.append(node)

    def init_tree(self, parent_tag: str = ""):
        """
        Рекурсивно присваивает снежные теги и вызывает elem.init(tag).
        """
        # Формируем снежный тег
        self.tag = f"{parent_tag}_{self.name}" if parent_tag else self.name

        # Инициализируем элемент, если он есть
        if self.elem is not None:
            self.elem.init(self.tag)  # публичный init с проверкой __is_init

        # Рекурсивно инициализируем детей
        for child in self.children:
            child.init_tree(self.tag)

    def build_tree(self) -> Html:
        """
        Рекурсивно строит HTML снизу вверх.
        Возвращает готовую HTML-строку этого узла.
        """
        # 1. Строим всех детей
        children_data: List[Tuple[ElementTag, Html]] = [
            (child.tag, child.build_tree()) for child in self.children
        ]

        if self.elem is not None:
            # 2. Готовим дополнительные kwargs для ready (например, tab_titles)
            extra_kwargs = self._collect_extra_kwargs()
            # 3. Передаём детей элементу (фаза ready)
            self.elem.ready(children_data, **extra_kwargs)
            # 4. Вызываем финальную сборку (фаза build) и возвращаем результат
            self.elem.build()
            return self.elem.get_result()
        else:
            # Если узлу не назначен элемент, просто склеиваем HTML детей
            return "".join(html for _, html in children_data)

    def _collect_extra_kwargs(self) -> dict:
        """
        Собирает дополнительные параметры, которые нужны конкретному элементу.
        Например, TabsElement ожидает tab_titles.
        Использует self.children (список SiteNode) для доступа к метаданным.
        """
        extra = {}
        if self.elem is not None and hasattr(self.elem, '_tab_titles'):
            # Для табов передаём заголовки вкладок из метаданных детей
            tab_titles = [child.meta.get('tab_title', child.name) for child in self.children]
            extra['tab_titles'] = tab_titles
        return extra