# project/build.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.page_elements import (
    TextElement, SectionElement, TabsElement,
    CardElement, TechTagElement, ButtonElement,
    ModalElement, ModalContainerElement,
    AccordionElement, AccordionItemElement
)
from core.page_nodes import SiteNode
from core.page_builders import SiteBuilder
from core.page_di_tools import FileDI  # инъектор зависимостей


# ----------------------------------------------------------------------
# Настройка инъектора для загрузки Markdown-файлов
# ----------------------------------------------------------------------
# Указываем базовую папку для поиска контента — папка project/
FileDI.load_directory = Path(__file__).parent

# Фабрики для загрузки превью и полного описания проектов
def load_preview(project_name: str) -> FileDI:
    """Создаёт TextElement, наполненный содержимым preview.md проекта."""
    return FileDI(
        TextElement,
        load_first=True,
        content=Path("content") / "projects" / project_name / "preview.md"
    )

def load_presentation(project_name: str) -> FileDI:
    """Создаёт TextElement, наполненный содержимым presentation.md проекта."""
    return FileDI(
        TextElement,
        load_first=True,
        content=Path("content") / "projects" / project_name / "presentation.md"
    )

def load_methodology(filename: str) -> FileDI:
    return FileDI(
        TextElement,
        load_first=True,
        content=Path("content") / "methodology" / filename
    )

# ----------------------------------------------------------------------
# Точка входа сборки
# ----------------------------------------------------------------------
def main():
    page = SiteNode("page")

    # ========================== ВКЛАДКИ ==========================
    tabs = SiteNode("maintabs", TabsElement())

    # ---------- 1. Методология ----------
    method_sec = SiteNode("methodology", SectionElement("Методология"),
                          meta={"tab_title": "Методология"})
    accordion = SiteNode("accordion", AccordionElement())

    # Порядок файлов и начальное состояние аккордеона
    method_items = [
        ("01_library_module.md", False),
        ("02_unbreakable_foundation.md", False),
        ("03_ai_native.md", False),
        ("04_plugin_first.md", False),
        ("05_extractable_code.md", False),
    ]

    for filename, open_default in method_items:
        # Загружаем содержимое .md через инъектор → получаем TextElement
        text_elem = load_methodology(filename)()
        # Аккордеон без заголовка (он уже есть в Markdown)
        item = SiteNode("item", AccordionItemElement("", open_by_default=open_default))
        item.add_child(SiteNode("content", text_elem))
        accordion.add_child(item)

    method_sec.add_child(accordion)
    tabs.add_child(method_sec)
    # ---------- 2. Проекты ----------
    proj_sec = SiteNode("projects", SectionElement("Проекты"),
                        meta={"tab_title": "Проекты"})

    # Вспомогательная функция для создания карточки проекта
    def add_project_card(section: SiteNode, project_name: str, title: str, tags: list[str]):
        card = SiteNode(f"{project_name}_card", CardElement(title, ""))
        # Загружаем превью через инъектор
        card.add_child(SiteNode("desc", load_preview(project_name)()))
        for tag in tags:
            card.add_child(SiteNode(f"tag_{tag}", TechTagElement(tag)))
        card.add_child(SiteNode("btn", ButtonElement("Подробнее", project_name)))
        section.add_child(card)

    add_project_card(proj_sec, "gunverse", "Gunverse",
                     ["GDScript", "ECS", "Zero-If"])
    add_project_card(proj_sec, "simulator", "Li-ion Battery Simulation",
                     ["Python", "DearPyGui", "Dataflow"])
    add_project_card(proj_sec, "qa_graph", "QA Graph Migrator",
                     ["Python", "State Monad", "PostgreSQL"])

    tabs.add_child(proj_sec)

    # ---------- 3. О себе ----------
    about_sec = SiteNode("about", SectionElement("О себе"),
                         meta={"tab_title": "О себе"})
    about_sec.add_child(SiteNode("bio", TextElement(
        "**5 лет** инженерной практики (2021–2026). Совмещал роли QA-архитектора, "
        "техлида игрового проекта, фрилансера и R&D-инженера.\n\n"
        "Бакалавр приборостроения (МГТУ им. Баумана), математическое самообразование "
        "(теория категорий, аппроксимация, тервер).\n\n"
        "Уверенный Linux (Arch), английский B1 (техническая документация)."
    )))
    tabs.add_child(about_sec)

    # ---------- 4. Контакты ----------
    contact_sec = SiteNode("contact", SectionElement("Контакты"),
                           meta={"tab_title": "Контакты"})
    contacts = [
        "📧 [xseo.22.24vl@gmail.com](mailto:xseo.22.24vl@gmail.com)",
        "💬 Telegram: [@Xseo_Tristielles](https://t.me/Xseo_Tristielles)",
        "🐙 GitHub: [mrXseo](https://github.com/mrXseo)",
        "📍 Россия, UTC+3",
    ]
    for contact_text in contacts:
        contact_sec.add_child(SiteNode("info", TextElement(contact_text)))
    tabs.add_child(contact_sec)

    page.add_child(tabs)

    # ========================== МОДАЛЬНЫЕ ОКНА ==========================
    modals_container = SiteNode("modals", ModalContainerElement())

    # Функция для создания модального окна с презентацией
    def add_modal(container: SiteNode, project_name: str, title: str):
        modal = SiteNode(f"modal_{project_name}", ModalElement(project_name, title))
        # Загружаем полное описание через инъектор
        modal.add_child(SiteNode("body", load_presentation(project_name)()))
        container.add_child(modal)

    add_modal(modals_container, "gunverse", "Gunverse — компонентный фреймворк")
    add_modal(modals_container, "simulator", "Li-ion Battery Simulation")
    add_modal(modals_container, "qa_graph", "QA Graph Migrator")

    page.add_child(modals_container)

    # ========================== СБОРКА ==========================
    builder = SiteBuilder(Path(__file__).parent)
    output_file = Path("index.html")
    builder.build(page, output_path=str(output_file), page_title="XSEO")
    abs_path = output_file.resolve()
    size_bytes = abs_path.stat().st_size
    print(f"Сайт собран: {abs_path}")
    print(f"Размер: {size_bytes} байт")


if __name__ == "__main__":
    main()