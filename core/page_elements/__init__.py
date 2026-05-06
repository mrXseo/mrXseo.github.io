from abc import ABC, abstractmethod

class Element(ABC):
    """Базовый контейнер для любого элемента страницы (уровень 2)."""
    @abstractmethod
    def render(self, context) -> str:
        ...

class Paragraph(Element):
    def __init__(self, text: str):
        self.text = text

    def render(self, context) -> str:
        # пока не используем mistune, просто plain text в <p>
        return f"<p>{self.text}</p>"

class Image(Element):
    def __init__(self, src: str, alt: str = ""):
        self.src = src
        self.alt = alt

    def render(self, context) -> str:
        # context позже даст правильный путь к ресурсу
        url = context.resolve_asset(self.src)
        return f'<img src="{url}" alt="{self.alt}">'