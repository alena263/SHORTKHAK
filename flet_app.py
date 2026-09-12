import os
import time
import datetime
import flet as ft
import requests
import html
import threading
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные окружения из .env файла (локально)


API_KEY = os.getenv("API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")
API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
MODEL_URI = f"gpt://{FOLDER_ID}/yandexgpt-lite/latest" if FOLDER_ID else None

# Адрес опубликованного сайта — агент подгружает те же JSON-файлы,
# что использует сам сайт для календаря и расписания. Если адрес сайта
# изменится, поменяйте его здесь (или через переменную окружения SITE_BASE_URL).
SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "https://alena263.github.io/SHORTKHAK")
EVENTS_URL = f"{SITE_BASE_URL}/data/events.json"
SCHEDULE_URL = f"{SITE_BASE_URL}/data/schedule.json"

_context_cache = {"text": None, "fetched_at": 0}
CONTEXT_TTL_SECONDS = 300  # обновлять данные сайта не чаще раза в 5 минут


def _format_events(events):
    if not events:
        return "нет данных о мероприятиях"
    lines = []
    for e in events:
        parts = [e.get("date", ""), e.get("time", "")]
        header = " ".join(p for p in parts if p)
        line = f"- {header}: {e.get('title', '')}"
        if e.get("location"):
            line += f", место: {e['location']}"
        if e.get("description"):
            line += f" — {e['description']}"
        lines.append(line)
    return "\n".join(lines)


def _format_schedule(schedule):
    days = (schedule or {}).get("days", {})
    if not days:
        return "нет данных о расписании"
    lines = []
    for day, lessons in days.items():
        for lesson in lessons:
            lines.append(
                f"- {day}, {lesson.get('time', '')}: {lesson.get('subject', '')} "
                f"(группа {lesson.get('group', '')}), ауд. {lesson.get('room', '')}, "
                f"преподаватель {lesson.get('teacher', '')}"
            )
    return "\n".join(lines)


def get_site_context():
    now = time.time()
    if _context_cache["text"] and now - _context_cache["fetched_at"] < CONTEXT_TTL_SECONDS:
        return _context_cache["text"]

    try:
        events = requests.get(EVENTS_URL, timeout=10).json()
    except Exception:
        events = []
    try:
        schedule = requests.get(SCHEDULE_URL, timeout=10).json()
    except Exception:
        schedule = {}

    today = datetime.date.today().isoformat()
    text = (
        "Ты — помощник сайта университета «Университет успеха, славы и богатства» (УУСБ). "
        f"Сегодняшняя дата: {today}. "
        "Отвечай на вопросы студентов и абитуриентов кратко и по делу, опираясь на "
        "приведённые ниже данные сайта. Если в вопросе спрашивают то, чего нет в "
        "данных — честно скажи, что не располагаешь такой информацией.\n\n"
        f"Мероприятия:\n{_format_events(events)}\n\n"
        f"Расписание занятий:\n{_format_schedule(schedule)}"
    )

    _context_cache["text"] = text
    _context_cache["fetched_at"] = now
    return text


def format_error(exc):
    msg = str(exc).lower()
    if '401' in str(exc) or 'auth' in msg or 'invalid api' in msg or 'api key' in msg or 'authentication' in msg:
        return "Ошибка Yandex Cloud: API key или авторизация не приняты. Проверьте ключ и права в облаке."
    return str(exc)


def call_yandex(question, on_success, on_error):
    def worker():
        try:
            if not API_KEY or not FOLDER_ID:
                raise Exception("Не заданы переменные окружения API_KEY / FOLDER_ID")
            headers = {
                "Authorization": f"Api-Key {API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "modelUri": MODEL_URI,
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.7,
                    "maxTokens": "1000",
                },
                "messages": [
                    {"role": "system", "text": get_site_context()},
                    {"role": "user", "text": question},
                ],
            }
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            if response.status_code == 401:
                raise Exception("401 Unauthorized: API key is invalid")
            if response.status_code == 403:
                raise Exception("403 Forbidden: folder or API key permission denied")
            if response.status_code == 429:
                raise Exception("429 RESOURCE_EXHAUSTED: quota exceeded")
            if response.status_code >= 400:
                try:
                    details = response.json()
                except ValueError:
                    details = response.text
                raise Exception(f"{response.status_code} error: {details}")
            data = response.json()
            text = data["result"]["alternatives"][0]["message"]["text"]
            on_success(question, text)
        except Exception as exc:
            on_error(format_error(exc))

    threading.Thread(target=worker, daemon=True).start()


def main(page: ft.Page):
    page.title = "Ассистент"
    page.window.width = 600
    page.window.height = 420
    page.window.resizable = False
    page.window.bgcolor = "maroon"
    page.bgcolor = "maroon"
    page.padding = 10
    page.scroll = "hidden"

    history = ft.Column(scroll="auto", width=560, height=270, spacing=4)
    status = ft.Text("Готов", size=16, weight="bold", color="#a6ffd7", font_family="Times New Roman")
    question_label = ft.Text("Ваш вопрос:", size=17, weight="bold", color="black", font_family="Times New Roman")

    question = ft.TextField(
        hint_text="Напишите вопрос для ассистента УУСБ...",
        width=560,
        height=30,
        border_radius=4,
        border_color="#d0d0d0",
        text_align=ft.TextAlign.LEFT,
    )
    question.bgcolor = "white"

    ask_button = ft.Button(
        content=ft.Text("Спросить", size=17, italic=True, font_family="Times New Roman", color="white"),
        width=560,
        height=30,
        bgcolor="#4d4d4d",
        color="white",
    )

    def add_history_message(who, text):
        clean_text = html.escape(text)
        if who == "user":
            bubble = ft.Container(
                content=ft.Text(clean_text, size=15, color="#1c6f2c", font_family="Times New Roman"),
                bgcolor="#d9fdd3",
                border=ft.Border.all(1, "#9ad789"),
                padding=8,
                border_radius=4,
                alignment=ft.Alignment.CENTER_LEFT,
            )
            history.controls.append(bubble)
        else:
            bubble = ft.Container(
                content=ft.Text(clean_text, size=15, color="#303030", font_family="Times New Roman"),
                bgcolor="#f0f0f0",
                border=ft.Border.all(1, "#d0d0d0"),
                padding=8,
                border_radius=4,
                alignment=ft.Alignment.CENTER_LEFT,
            )
            history.controls.append(bubble)

        page.update()

    def ask(e):
        q = question.value.strip()
        if not q:
            status.value = "Введите вопрос сначала."
            status.color = "red"
            page.update()
            return

        ask_button.disabled = True
        status.value = "Загрузка..."
        status.color = "orange"
        page.update()

        def on_success(user_q, answer):
            add_history_message("user", user_q)
            add_history_message("yandex", answer)
            status.value = "Готов"
            status.color = "green"
            ask_button.disabled = False
            question.value = ""
            page.update()

        def on_error(message):
            add_history_message("yandex", message)
            status.value = "Ошибка"
            status.color = "red"
            ask_button.disabled = False
            page.update()

        call_yandex(q, on_success, on_error)

    ask_button.on_click = ask

    page.add(
        ft.Column([
            ft.Container(
                content=history,
                width=560,
                height=270,
                bgcolor="white",
                border=ft.Border.all(1, "#d0d0d0"),
                padding=5,
                border_radius=4,
            ),
            ft.Column([
                ft.Row([status], alignment="start"),
                ft.Row([question_label], alignment="start"),
            ], spacing=2),
            question,
            ask_button,
        ],
        width=560,
        spacing=2,
        )
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    ft.run(main, host="0.0.0.0", port=port)
