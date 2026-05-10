from .page_element import PageElement, ElementTag, Html
from typing import List, Tuple


class TechTagElement(PageElement):
    """Маленький тег технологии."""
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        self.result_html = f'<span class="tech-tag">{self.text}</span>'


class MetricElement(PageElement):
    """Блок метрики (для модалок и не только)."""
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        self.result_html = f'<span class="metric">{self.text}</span>'