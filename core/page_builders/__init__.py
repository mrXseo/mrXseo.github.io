from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from ..page_nodes import SiteNode

class SiteBuilder:
    def __init__(self, project_root : str = "", template_dir: str = "templates"):
        self.project_root = project_root or Path().cwd() / "project"
        template_path = project_root / template_dir
        self.env = Environment(loader=FileSystemLoader(str(template_path)))

    def build(self, root : SiteNode, output_path: str = "index.html",
              template_name: str = "base.html", **template_vars) -> str:
        root.init_tree()
        content = root.build_tree()
        template = self.env.get_template(template_name)
        html = template.render(content=content, **template_vars)
        out = self.project_root / Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')
        return html