

import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
DATA_DIR = ROOT / "data"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"


def load_json(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def build():
    events = load_json("events.json")
    schedule = load_json("schedule.json")

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

    # Очищаем и пересоздаём папку вывода
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    pages = {
        "index.html": {"active": "home"},
        "calendar.html": {"active": "calendar"},
        "schedule.html": {"active": "schedule", "schedule": schedule},
    }

    for filename, context in pages.items():
        template = env.get_template(filename)
        html = template.render(**context)
        (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
        print(f"  собрано: {filename}")

    # Копируем статические файлы и данные, чтобы JS мог их подгружать
    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")
    shutil.copytree(DATA_DIR, OUTPUT_DIR / "data")

    # Файл .nojekyll нужен, чтобы GitHub Pages не пытался обработать
    # сайт через Jekyll (это может сломать папки, начинающиеся с "_")
    (OUTPUT_DIR / ".nojekyll").touch()

    print(f"\nГотово. Сайт собран в папке: {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
