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