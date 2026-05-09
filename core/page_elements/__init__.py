from abc import ABC, abstractmethod

class PageElement(ABC):
    def __init__(self, tag: str = ""):
        self.tag = tag

    @abstractmethod
    def init(self, tag: str, **kwargs):
        self.tag = tag

    @abstractmethod
    def ready(self, children: list[tuple[object, str]], **kwargs):
        """
        children – список кортежей (child_node, child_html).
        child_node – это SiteNode, у которого мы можем взять meta, tag и т.д.
        child_html – готовый HTML дочернего узла.
        """
        ...

    @abstractmethod
    def build(self) -> str:
        ...


class TextElement(PageElement):
    def __init__(self, content: str):
        super().__init__()
        self.content = content
        self.html = ""

    def init(self, tag: str, **kwargs):
        super().init(tag, **kwargs)

    def ready(self, children: list = [], **kwargs):
        import mistune
        md = mistune.create_markdown()
        self.html = f'<div id="{self.tag}">{md(self.content)}</div>'

    def build(self) -> str:
        return self.html


class CardElement(PageElement):
    def __init__(self, title: str, description: str):
        super().__init__()
        self.title = title
        self.description = description
        self.html = ""

    def init(self, tag: str, **kwargs):
        super().init(tag, **kwargs)

    def ready(self, children: list = [], **kwargs):
        # Для карточки просто берём HTML первого ребёнка, если есть
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
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.html = ""

    def init(self, tag: str, **kwargs):
        super().init(tag, **kwargs)

    def ready(self, children: list = [], **kwargs):
        children_html = "".join(child_html for _, child_html in children)
        self.html = f'''
        <section id="{self.tag}">
            <h2>{self.title}</h2>
            {children_html}
        </section>'''

    def build(self) -> str:
        return self.html


class TabsElement(PageElement):
    """Контейнер вкладок – сам строит кнопки и панели."""
    def __init__(self):
        super().__init__()
        self.html = ""

    def init(self, tag: str, **kwargs):
        super().init(tag, **kwargs)

    def ready(self, children: list[tuple[object, str]], **kwargs):
        # children – список (SiteNode, html), где node.meta['tab_title'] содержит заголовок
        buttons = []
        panes = []
        for i, (child_node, child_html) in enumerate(children):
            title = child_node.meta.get("tab_title", child_node.name)
            active_class = "active" if i == 0 else ""
            # Кнопка
            buttons.append(
                f'<button class="tab-btn {active_class}" onclick="switchTab(\'{child_node.tag}\')">{title}</button>'
            )
            # Панель
            panes.append(
                f'<div class="tab-pane {active_class}" id="{child_node.tag}">{child_html}</div>'
            )
        self.html = f'''
        <div class="tabs-container" id="{self.tag}">
            <div class="tabs">{"".join(buttons)}</div>
            {"".join(panes)}
        </div>'''

    def build(self) -> str:
        return self.html