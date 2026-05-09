# project/core/page_elements/__init__.py

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Базовый класс
# ---------------------------------------------------------------------------

class PageElement(ABC):
    """Контейнер: владеет только своим HTML, живёт в трёх фазах."""
    def __init__(self) -> None:
        self.tag: str = ""

    # ------------------------------------------------------------------
    # Жизненный цикл
    # ------------------------------------------------------------------

    @abstractmethod
    def init(self, tag: str, **kwargs) -> None:
        """Фаза 1: получить тег, подготовить шаблоны."""
        self.tag = tag

    @abstractmethod
    def ready(self, children: List[Tuple['SiteNode', str]], **kwargs) -> None:
        """Фаза 2: позднее связывание – дети уже отрендерены."""
        ...

    @abstractmethod
    def build(self) -> str:
        """Фаза 3: вернуть финальный HTML."""
        ...


# ---------------------------------------------------------------------------
# Вспомогательный класс – узел (forward reference)
# ---------------------------------------------------------------------------

class _SiteNode:  # forward declaration – настоящий SiteNode лежит в page_nodes
    name: str
    tag: str
    meta: dict
    elem: Optional[PageElement]
    children: List['_SiteNode']


SiteNode = _SiteNode  # для аннотаций


# ============================================================================
# СУЩЕСТВУЮЩИЕ ЭЛЕМЕНТЫ (БЕЗ ИЗМЕНЕНИЙ)
# ============================================================================

class TextElement(PageElement):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content = content
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        import mistune
        md = mistune.create_markdown()
        self.html = f'<div id="{self.tag}">{md(self.content)}</div>'

    def build(self) -> str:
        return self.html


class CardElement(PageElement):
    def __init__(self, title: str, description: str) -> None:
        super().__init__()
        self.title = title
        self.description = description
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        child_html = children[0][1] if children else ""
        self.html = f'''
        <div class="card" id="{self.tag}">
            <h3>{self.title}</h3>
            <p>{self.description}</p>
            {child_html}
        </div>'''

    def build(self) -> str:
        return self.html


class SectionElement(PageElement):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        children_html = "".join(child_html for _, child_html in children)
        self.html = f'''
        <section id="{self.tag}">
            <h2>{self.title}</h2>
            {children_html}
        </section>'''

    def build(self) -> str:
        return self.html


class TabsElement(PageElement):
    def __init__(self) -> None:
        super().__init__()
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        buttons = []
        panes = []
        for i, (child_node, child_html) in enumerate(children):
            title = child_node.meta.get("tab_title", child_node.name)
            active_class = "active" if i == 0 else ""
            buttons.append(
                f'<button class="tab-btn {active_class}" '
                f'onclick="switchTab(\'{child_node.tag}\')">{title}</button>'
            )
            panes.append(
                f'<div class="tab-pane {active_class}" id="{child_node.tag}">'
                f'{child_html}</div>'
            )
        self.html = f'''
        <div class="tabs-container" id="{self.tag}">
            <div class="tabs">{"".join(buttons)}</div>
            {"".join(panes)}
        </div>'''

    def build(self) -> str:
        return self.html


# ============================================================================
# НОВЫЕ ЭЛЕМЕНТЫ ДЛЯ ПОЛНОГО reference.html
# ============================================================================

class AccordionElement(PageElement):
    """Контейнер, который оборачивает детей в карточку с аккордеонами."""
    def __init__(self) -> None:
        super().__init__()
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        items_html = "".join(child_html for _, child_html in children)
        self.html = f'<div class="card" id="{self.tag}">{items_html}</div>'

    def build(self) -> str:
        return self.html


class AccordionItemElement(PageElement):
    """Один элемент аккордеона: заголовок + раскрывающийся контент."""
    def __init__(self, title: str, open_by_default: bool = False) -> None:
        super().__init__()
        self.title = title
        self.open = open_by_default
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        child_html = "".join(html for _, html in children)
        header_class = "accordion-header"
        body_class = "accordion-body"
        body_style = ""
        if self.open:
            header_class += " open"
            body_class += " open"
            body_style = f'max-height: {20}rem;'  # будет переопределено JS
        self.html = f'''
        <div class="accordion-item">
          <button class="{header_class}">{self.title}</button>
          <div class="{body_class}" style="{body_style}">
            <div class="accordion-content">{child_html}</div>
          </div>
        </div>'''

    def build(self) -> str:
        return self.html


class ButtonElement(PageElement):
    """Кнопка, которая открывает модальное окно."""
    def __init__(self, label: str, target_modal_id: str) -> None:
        super().__init__()
        self.label = label
        self.target = target_modal_id  # без префикса modal-
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        # кнопка не использует children
        self.html = (
            f'<button class="btn" onclick="openModal(\'{self.target}\')">'
            f'{self.label}</button>'
        )

    def build(self) -> str:
        return self.html


class ModalElement(PageElement):
    """Модальное окно."""
    def __init__(self, modal_id: str, title: str) -> None:
        super().__init__()
        self.modal_id = modal_id   # без префикса modal-
        self.title = title
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        body_html = "".join(html for _, html in children)
        self.html = f'''
        <div class="modal" id="modal-{self.modal_id}">
          <div class="modal-content">
            <button class="modal-close"
                    onclick="closeModal(\'{self.modal_id}\')">&times;</button>
            <h2>{self.title}</h2>
            {body_html}
          </div>
        </div>'''

    def build(self) -> str:
        return self.html


class TechTagElement(PageElement):
    """Маленький тег технологии."""
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        self.html = f'<span class="tech-tag">{self.text}</span>'

    def build(self) -> str:
        return self.html


class MetricElement(PageElement):
    """Блок метрики (для модалок и не только)."""
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        self.html = f'<span class="metric">{self.text}</span>'

    def build(self) -> str:
        return self.html


class ModalContainerElement(PageElement):
    """Невидимый контейнер для сбора всех модальных окон в конце страницы."""
    def __init__(self) -> None:
        super().__init__()
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)

    def ready(self,
              children: List[Tuple[SiteNode, str]] = None,
              **kwargs) -> None:
        children = children or []
        self.html = "".join(html for _, html in children)

    def build(self) -> str:
        return self.html

# ============================================================================
# НОВЫЕ ЭЛЕМЕНТЫ ДЛЯ ПОЛНОГО reference.html
# ============================================================================

import os
from pathlib import Path

class MarkdownFileElement(PageElement):
    """Элемент, загружающий Markdown-файл и отображающий его как HTML."""
    def __init__(self, file_path: str) -> None:
        super().__init__()
        # путь относительно папки project/
        self.file_path = file_path
        self.html: str = ""

    def init(self, tag: str, **kwargs) -> None:
        super().init(tag, **kwargs)
        # Строим полный путь: от корня проекта (project/)
        base_dir = Path(__file__).parent.parent  # project/core/.. = project/
        full_path = base_dir / self.file_path
        if not full_path.exists():
            self.html = f'<div id="{self.tag}"><p>File not found: {self.file_path}</p></div>'
            return
        raw_md = full_path.read_text(encoding='utf-8')
        import mistune
        md = mistune.create_markdown()
        self.html = f'<div id="{self.tag}">{md(raw_md)}</div>'

    def ready(self, children: List[Tuple[SiteNode, str]] = None, **kwargs) -> None:
        # Уже всё готово после init, можно не переопределять
        pass

    def build(self) -> str:
        return self.html