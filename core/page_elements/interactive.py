from .page_element import PageElement, ElementTag, Html
from typing import List, Tuple, Optional


class TabsElement(PageElement):
    """Контейнер вкладок: генерирует кнопки и панели на основе дочерних узлов."""
    def __init__(self) -> None:
        super().__init__()
        self._tab_titles: List[str] = []

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        # Ожидаем, что сборщик передаст список заголовков вкладок через kwargs
        self._tab_titles = kwargs.get('tab_titles', [])

    def _build(self, **kwargs) -> None:
        buttons = []
        panes = []
        for i, (child_tag, child_html) in enumerate(self.children):
            # Используем переданный заголовок или, если его нет, идентификатор вкладки
            title = self._tab_titles[i] if i < len(self._tab_titles) else child_tag
            active_class = "active" if i == 0 else ""
            buttons.append(
                f'<button class="tab-btn {active_class}" data-tab="{child_tag}">{title}</button>'
            )
            panes.append(
                f'<div class="tab-pane {active_class}" id="{child_tag}">{child_html}</div>'
            )
        self.result_html = f'''
        <div class="tabs-container" id="{self.tag}">
            <div class="tabs">{"".join(buttons)}</div>
            {"".join(panes)}
        </div>'''


class ButtonElement(PageElement):
    """Кнопка, открывающая модальное окно."""
    def __init__(self, label: str, target_id: str) -> None:
        super().__init__()
        self.label = label
        self.target_id = target_id  # без префикса modal-

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        self.result_html = (
            f'<button class="btn" onclick="openModal(\'{self.target_id}\')">'
            f'{self.label}</button>'
        )


class ModalElement(PageElement):
    """Модальное окно с заголовком, кнопкой закрытия и вложенным контентом."""
    def __init__(self, modal_id: str, title: str) -> None:
        super().__init__()
        self.modal_id = modal_id  # без префикса modal-
        self.title = title

    def _init(self, **kwargs) -> None:
        pass

    def _ready(self, **kwargs) -> None:
        pass

    def _build(self, **kwargs) -> None:
        body_html = "".join(html for _, html in self.children)
        self.result_html = f'''
        <div class="modal" id="modal-{self.modal_id}">
          <div class="modal-content">
            <button class="modal-close"
                    onclick="closeModal(\'{self.modal_id}\')">&times;</button>
            <h2>{self.title}</h2>
            {body_html}
          </div>
        </div>'''