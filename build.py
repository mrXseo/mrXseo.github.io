import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "project"))

from core.page_elements import TextElement, CardElement, SectionElement, TabsElement
from core.page_nodes import SiteNode

# Корень
page = SiteNode("page")

# Вкладки
tabs = SiteNode("maintabs", TabsElement())

# Вкладка 1: Методология
sec1 = SiteNode("methodology", SectionElement("Методология"), meta={"tab_title": "Методология"})
sec1.add_child(SiteNode("desc", TextElement("**Библиотечный модуль**, **Нерушимый фундамент**, **AI‑Native дизайн**.")))
tabs.add_child(sec1)

# Вкладка 2: Проекты
sec2 = SiteNode("projects", SectionElement("Проекты"), meta={"tab_title": "Проекты"})
sec2.add_child(SiteNode("gunverse", CardElement("Gunverse", "Компонентный фреймворк для игровых механик.")))
sec2.add_child(SiteNode("liion", CardElement("Li-ion Sim", "Научный комплекс моделирования батарей.")))
tabs.add_child(sec2)

# Вкладка 3: О себе
sec3 = SiteNode("about", SectionElement("О себе"), meta={"tab_title": "О себе"})
sec3.add_child(SiteNode("bio", TextElement("5 лет инженерной практики, математический бэкграунд, бакалавр приборостроения.")))
tabs.add_child(sec3)

page.add_child(tabs)

# Инициализация и сборка
page.init_tree()
html_content = page.build_tree()

# Вставка в шаблон (теперь добавим стили и скрипт)
full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>XSEO</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, sans-serif; color: #1a1a1a; background: #f5f7fa; line-height: 1.5; }}
    .container {{ max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem; }}
    header {{ text-align: center; padding: 3rem 0 2rem; }}
    h1 {{ font-size: 2.8rem; font-weight: 700; margin-bottom: 0.3rem; }}
    .subtitle {{ font-size: 1.3rem; color: #555; }}
    .tabs {{ display: flex; justify-content: center; gap: 1rem; margin: 2.5rem 0 1rem; flex-wrap: wrap; }}
    .tab-btn {{ background: #e2e6ea; border: none; padding: 0.7rem 1.8rem; border-radius: 2rem; font-size: 1rem; cursor: pointer; transition: 0.2s; }}
    .tab-btn.active {{ background: #0f1626; color: white; }}
    .tab-btn:hover:not(.active) {{ background: #cfd5db; }}
    .tab-pane {{ display: none; animation: fade 0.3s; }}
    .tab-pane.active {{ display: block; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .card {{ background: white; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 6px 18px rgba(0,0,0,0.05); }}
    footer {{ text-align: center; padding: 2rem 0; color: #777; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>XSEO</h1>
      <div class="subtitle">Systems Architect</div>
      <p>Нерушимые фундаменты для сложных систем</p>
    </header>
    {html_content}
  </div>
  <footer>&copy; 2026 XSEO</footer>
  <script>
    function switchTab(targetId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      const pane = document.getElementById(targetId);
      if (pane) pane.classList.add('active');
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        if (btn.getAttribute('onclick')?.includes(`'${{targetId}}'`)) btn.classList.add('active');
      }});
    }}
  </script>
</body>
</html>"""

out = Path("project/output/index.html")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(full_html, encoding="utf-8")
print(f"Сайт собран: {len(full_html)} байт")