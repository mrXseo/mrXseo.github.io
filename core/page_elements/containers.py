# project/core/page_elements/containers.py

from typing import List, Tuple
from .page_element import PageElement, ElementTag, Html
import re


class SectionElement(PageElement):
    """Оборачивает дочерние элементы в <section> с заголовком."""
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        # Дети уже в self.children, дополнительных действий не нужно
        pass

    def _build(self, **kwargs) -> None:
        children_html = "".join(html for _, html in self.children)
        self.result_html = f'''
        <section id="{self.tag}">
            <h2>{self.title}</h2>
            {children_html}
        </section>'''


class CardElement(PageElement):
    def __init__(self, title: str, description: str = "") -> None:
        super().__init__()
        self.title = title
        self.description = description

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        # Рендерим всех детей подряд – описание, теги, кнопку
        children_html = "".join(html for _, html in self.children)
        self.result_html = f'''
        <div class="card" id="{self.tag}">
            <h3>{self.title}</h3>
            <p>{self.description}</p>
            {children_html}
        </div>'''


class AccordionElement(PageElement):
    """Группирует элементы аккордеона внутри карточки."""
    def __init__(self) -> None:
        super().__init__()

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        items_html = "".join(html for _, html in self.children)
        self.result_html = f'<div class="card" id="{self.tag}">{items_html}</div>'


class AccordionItemElement(PageElement):
    """Элемент аккордеона: заголовок + раскрывающееся содержимое."""
    def __init__(self, title: str, open_by_default: bool = False) -> None:
        super().__init__()
        self.title = title
        self.open_by_default = open_by_default

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        child_html = "".join(html for _, html in self.children)
        
        # Если заголовок не задан явно, пытаемся извлечь его из первого <h3>
        if not self.title:
            match = re.search(r'<h3>(.*?)</h3>', child_html)
            if match:
                self.title = match.group(1)  # текст заголовка
                # Убираем первый <h3> из тела, чтобы не дублировался
                child_html = child_html.replace(match.group(0), '', 1)
        
        # Классы и начальное состояние
        header_class = "accordion-header"
        body_class = "accordion-body"
        body_style = ""
        if self.open_by_default:
            header_class += " open"
            body_class += " open"
            body_style = 'max-height: 20rem;'
        
        # Генерируем кнопку-заголовок, если заголовок есть, иначе просто тело
        if self.title:
            self.result_html = f'''
            <div class="accordion-item">
              <button class="{header_class}">{self.title}</button>
              <div class="{body_class}" style="{body_style}">
                <div class="accordion-content">{child_html}</div>
              </div>
            </div>'''
        else:
            # Заголовок не задан и не найден в контенте — выводим только содержимое
            self.result_html = f'''
            <div class="accordion-item">
              <div class="accordion-content">{child_html}</div>
            </div>'''

class ModalContainerElement(PageElement):
    """Прозрачный контейнер для сбора модальных окон в конце страницы."""
    def __init__(self) -> None:
        super().__init__()

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        self.result_html = "".join(html for _, html in self.children)