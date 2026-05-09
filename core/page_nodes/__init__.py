from ..page_elements import PageElement

class SiteNode:
    def __init__(self, name: str, elem: PageElement = None, meta: dict = None):
        self.name = name
        self.elem = elem
        self.children: list['SiteNode'] = []
        self.meta = meta or {}
        self.tag = ""

    def add_child(self, node: 'SiteNode'):
        self.children.append(node)

    def init_tree(self, parent_tag: str = ""):
        self.tag = f"{parent_tag}_{self.name}" if parent_tag else self.name
        if self.elem:
            self.elem.init(self.tag)
        for child in self.children:
            child.init_tree(self.tag)

    def build_tree(self) -> str:
        # Сначала строим детей
        children_data = [(child, child.build_tree()) for child in self.children]

        if self.elem:
            self.elem.ready(children_data)
            return self.elem.build()
        else:
            # Если узлу не назначен элемент, просто склеиваем HTML детей
            return "".join(html for _, html in children_data)