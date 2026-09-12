"""
app.py — маленький бэкенд для ИИ-агента сайта.

Зачем он нужен: GitHub Pages отдаёт только статику и не может хранить
секреты. Ключ API Yandex Cloud должен лежать на отдельном сервере —
здесь он читается из переменных окружения (YANDEX_API_KEY,
YANDEX_FOLDER_ID), а не из кода. Сайт обращается к этому серверу через
обычный POST-запрос, сервер обращается к Yandex Cloud и возвращает ответ.

Локальный запуск:
    pip install -r requirements.txt
    set YANDEX_API_KEY=...      (Windows)  /  export YANDEX_API_KEY=...  (macOS/Linux)
    set YANDEX_FOLDER_ID=...
    python app.py

Деплой — см. README.md в этой папке.
"""

import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# На старте разрешаем запросы с любого адреса, чтобы всё быстро заработало.
# Когда сайт опубликуется на GitHub Pages, лучше ограничить ALLOWED_ORIGIN
# точным адресом сайта — см. README.md.
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/api/chat", methods=["OPTIONS"])
def chat_preflight():
    return ("", 204)

API_KEY = os.environ.get("YANDEX_API_KEY")
FOLDER_ID = os.environ.get("YANDEX_FOLDER_ID")
API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def format_error(exc: Exception) -> str:
    msg = str(exc).lower()
    if "401" in str(exc) or "auth" in msg or "api key" in msg:
        return "Ошибка Yandex Cloud: ключ API не принят. Проверьте YANDEX_API_KEY."
    if "403" in str(exc):
        return "Ошибка Yandex Cloud: доступ запрещён. Проверьте права и YANDEX_FOLDER_ID."
    if "429" in str(exc):
        return "Превышена квота запросов к Yandex Cloud. Попробуйте чуть позже."
    return "Не удалось получить ответ от ИИ-агента. Попробуйте ещё раз."


def ask_yandex(question: str) -> str:
    if not API_KEY or not FOLDER_ID:
        raise RuntimeError("На сервере не заданы YANDEX_API_KEY / YANDEX_FOLDER_ID")

    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {"stream": False, "temperature": 0.7, "maxTokens": 1000},
        "messages": [{"role": "user", "text": question}],
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["result"]["alternatives"][0]["message"]["text"]


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    question = (body.get("message") or "").strip()
    if not question:
        return jsonify({"reply": "Пожалуйста, введите вопрос."}), 400
    try:
        answer = ask_yandex(question)
        return jsonify({"reply": answer})
    except Exception as exc:
        return jsonify({"reply": format_error(exc)}), 500


@app.route("/", methods=["GET"])
def health():
    # Используется для проверки, что сервис жив (и для "будильника" на бесплатных тарифах)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
