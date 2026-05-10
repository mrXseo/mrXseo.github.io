from abc import ABC, abstractmethod
from typing import List, Tuple, TypeAlias

Html : TypeAlias = str
ElementTag : TypeAlias = str

class UnBuildError(AttributeError):
    ...
class UnInitError(AttributeError):
    ...
class UnReadyError(AttributeError):
    ...

class PageElement(ABC):
    """Контейнер: владеет только своим HTML, живёт в трёх фазах."""
    def __init__(self) -> None:
        self.tag : ElementTag = ""
        self.result_html : Html = ""
        self.__is_build : bool = False
        self.__is_init : bool = False
        self.__is_ready : bool = False
        self.children : List[Tuple[ElementTag, Html]] = list()

    def get_result(self) -> Html:
        if not self.__is_build:
            raise UnBuildError
        return self.result_html

    def get_tag(self) -> ElementTag:
        if not self.__is_init:
            raise UnInitError
        return self.tag

    @abstractmethod
    def _init(self, **kwargs) -> None:
        ...

    def init(self, tag : ElementTag, **kwargs) -> None:
        """Фаза 1: получить тег, подготовить шаблоны."""
        self.tag = tag
        self._init(**kwargs)
        self.__is_init = True

    @abstractmethod
    def _ready(self, **kwargs) -> None:
        ...

    def ready(self, children: List[Tuple[ElementTag, Html]], **kwargs) -> None:
        """Фаза 2: позднее связывание – дети уже отрендерены."""
        if not self.__is_init:
            raise UnInitError
        self.children = children
        self._ready(**kwargs)
        self.__is_ready = True
    
    @abstractmethod
    def _build(self, **kwargs) -> None:
        ...
    
    def build(self, **kwargs) -> None:
        """Фаза 3: собрать финальный HTML."""
        if not self.__is_ready:
            raise UnReadyError
        self._build(**kwargs)
        self.__is_build = True
