# Бэкенд ИИ-агента (YandexGPT)

Маленький сервер на Flask: принимает вопрос от чат-виджета на сайте,
обращается к YandexGPT, возвращает ответ. Ключ API хранится в
переменных окружения хостинга — не в коде и не на GitHub.

## Прежде всего — перевыпустите ключ

Ключ, который был в `flet_app.py`, уже "засвечен". Зайдите в консоль
Yandex Cloud → сервисные аккаунты → API-ключи, отзовите старый и
создайте новый. Используйте только новый ключ дальше.

## Деплой на Render.com (бесплатный вариант, проще всего)

1. Положите папку `ai-backend` в свой GitHub-репозиторий — например,
   рядом с папкой `website` (в корне репозитория).
2. Зайдите на render.com, зарегистрируйтесь (можно через GitHub).
3. **New → Web Service** → выберите свой репозиторий.
4. Настройки:
   - **Root Directory**: `ai-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. В разделе **Environment** добавьте переменные:
   - `YANDEX_API_KEY` = ваш новый ключ
   - `YANDEX_FOLDER_ID` = ваш folder ID
6. Нажмите **Create Web Service** и дождитесь деплоя (несколько минут).
7. Скопируйте адрес вида `https://ваш-сервис.onrender.com` — рабочий
   URL чата будет `https://ваш-сервис.onrender.com/api/chat`.

Бесплатный тариф Render "засыпает" после ~15 минут без запросов, и
первый вопрос после паузы может обрабатываться до 30–60 секунд —
для учебного проекта это нормально.

## Подключение к сайту

В файле `website/static/js/ai_agent.js` впишите адрес в `endpoint`:

```js
const AI_AGENT_CONFIG = {
  endpoint: 'https://ваш-сервис.onrender.com/api/chat',
};
```

Закоммитьте и запушьте — виджет на сайте заработает.

## Локальная проверка перед деплоем

```
pip install -r requirements.txt
export YANDEX_API_KEY=ваш_ключ        # на Windows: set YANDEX_API_KEY=ваш_ключ
export YANDEX_FOLDER_ID=ваш_folder_id
python app.py
```

Проверить можно так:
```
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"Привет\"}"
```

## Ограничение доступа (по желанию)

Сейчас сервер отвечает любому сайту (`ALLOWED_ORIGIN=*`). Когда будете
знать точный адрес своего GitHub Pages, добавьте в Render переменную
окружения:

```
ALLOWED_ORIGIN=https://ваш-логин.github.io
```
