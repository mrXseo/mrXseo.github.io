from project.core.page_elements import Element

class Section(Element):
    """Композитный узел: содержит другие элементы (уровень 3)."""
    def __init__(self, title: str, children: list[Element] | None = None):
        self.title = title
        self.children = children or []

    def render(self, context) -> str:
        rendered_children = "\n".join(
            child.render(context) for child in self.children
        )
        return f"<section><h2>{self.title}</h2>{rendered_children}</section>"

class Page(Element):
    """Корневой узел страницы."""
    def __init__(self, title: str, sections: list[Section] | None = None):
        self.title = title
        self.sections = sections or []

    def render(self, context) -> str:
        # просто делегирует секциям, сами секции уже умеют рендерить своих детей
        rendered_sections = "\n".join(
            section.render(context) for section in self.sections
        )
        return rendered_sections