from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class PageBuilder:
    """Уровень 5: сборщик страницы."""
    def __init__(self, template_dir: str = "templates"):
        template_path = Path(__file__).parent.parent.parent / template_dir
        self.env = Environment(loader=FileSystemLoader(str(template_path)))

    def build(self, page, output_path: str = "output/index.html"):
        """Рендерит полную HTML-страницу и сохраняет на диск."""
        template = self.env.get_template("base.html")
        html = template.render(
            title=page.title,
            content=page.render(context={})  # контекст пока пустой
        )
        output_path : Path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        return html