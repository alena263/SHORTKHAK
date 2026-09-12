
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
