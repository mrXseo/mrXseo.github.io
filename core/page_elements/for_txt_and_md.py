from .page_element import PageElement, Html, ElementTag
from typing import List, Tuple
import mistune

class TextElement(PageElement):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content : str = content

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        md = mistune.create_markdown()        
        self.result_html = f'<div id="{self.tag}" class="md-content">{md(self.content)}</div>'
