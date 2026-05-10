from typing import Type, Dict, TypeAlias, Any
from pathlib import Path
from json import loads as read_json

AttributeName : TypeAlias = str

class FileDI:

    load_directory : Path = Path.cwd()
    _handlers = {
        ".txt" : lambda p: p.read_text(encoding='utf-8'),
        ".json" : lambda p: read_json(p.read_text(encoding='utf-8')),
        ".md" : lambda p: p.read_text(encoding='utf-8'),
    }

    def __init__(self, type : Type, load_first : bool = False, **kwargs : Path):
        self.type : Type = type
        self.di_kwargs : Dict[AttributeName, Path] = kwargs
        self.load_first : bool = load_first

    def __call__(self, **kwargs):
        load_kwargs : Dict[AttributeName, Any] = self.__collect()
        if self.load_first:
            combined = {**kwargs, **load_kwargs}
        else:
            combined = {**load_kwargs, **kwargs}
        return self.type(**combined)

    def __collect(self) -> Dict[AttributeName, Any]:
        result : Dict[AttributeName, Any] = dict()
        for attr_name, path in self.di_kwargs.items():
            if not (path.suffix in self._handlers):
                raise ValueError(
                    f"Нет обработчика для расширения '{path.suffix or '<no extension>'}' (файл: {path})"
                    )
            full_path = path if path.is_absolute() else self.load_directory / path
            result[attr_name] = self._handlers[path.suffix](full_path)
        return result