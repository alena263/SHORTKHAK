"""
add_event.py — быстро добавить мероприятие в data/events.json из терминала
и сразу пересобрать сайт.

Запуск:
    python add_event.py
Скрипт задаст несколько вопросов и сам обновит data/events.json,
после чего вызовет build.py.

Это самый простой способ "администрировать" мероприятия без правки
JSON вручную. После выполнения не забудьте закоммитить и запушить
изменения в GitHub.
"""

import json
from pathlib import Path

from build import build

EVENTS_PATH = Path(__file__).parent / "data" / "events.json"


def main():
    with open(EVENTS_PATH, encoding="utf-8") as f:
        events = json.load(f)

    print("Добавление нового мероприятия (Enter — оставить пустым)\n")
    title = input("Название: ").strip()
    date = input("Дата (ГГГГ-ММ-ДД): ").strip()
    time = input("Время (ЧЧ:ММ): ").strip()
    location = input("Место: ").strip()
    description = input("Описание: ").strip()

    new_id = max([e["id"] for e in events if isinstance(e["id"], int)], default=0) + 1
    events.append({
        "id": new_id,
        "title": title,
        "date": date,
        "time": time,
        "location": location,
        "description": description,
    })

    with open(EVENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    print("\nМероприятие добавлено в data/events.json. Пересобираю сайт...")
    build()


if __name__ == "__main__":
    main()
