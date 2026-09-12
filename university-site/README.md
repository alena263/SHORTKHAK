# Сайт университета

Учебный сайт с календарём мероприятий и расписанием занятий.
Собирается на Python (Jinja2), публикуется как статичный сайт на GitHub Pages.

## Как это устроено

GitHub Pages умеет отдавать только готовые файлы (HTML/CSS/JS) — Python-код
на сервере он не выполняет. Поэтому Python здесь используется как
**генератор сайта**:

```
data/            → исходные данные (JSON): мероприятия и расписание
templates/       → HTML-шаблоны (Jinja2)
static/          → CSS и JavaScript
build.py         → собирает templates/ + data/ → docs/
docs/            → готовый статичный сайт (создаётся сборкой, его и публикует GitHub Pages)
```

Интерактивность в браузере (переключение месяцев в календаре, вкладки
дней в расписании, добавление события) сделана на обычном JavaScript.

## Запуск и разработка в VS Code

1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
2. Соберите сайт:
   ```
   python build.py
   ```
3. Откройте `docs/index.html` через расширение VS Code **Live Server**
   (или командой `python -m http.server 8000` из папки `docs`, затем
   зайдите на `http://localhost:8000`).

## Как добавить мероприятие

Есть два способа:

**А. Через терминал (рекомендуется для постоянных, видимых всем событий)**
```
python add_event.py
```
Скрипт спросит название, дату, время, место и описание, добавит запись
в `data/events.json` и пересоберёт сайт. Дальше — обычный `git add`,
`git commit`, `git push`.

**Б. Прямо на сайте, кнопка «Добавить мероприятие» на странице календаря.**
Такое событие сохраняется в `localStorage` браузера — оно сразу видно
вам, но не появляется у других посетителей, потому что GitHub Pages не
имеет базы данных. Чтобы событие стало общим — перенесите его в
`data/events.json` через способ А.

## Как изменить расписание

Отредактируйте `data/schedule.json` (дни, группы, пары) и запустите
`python build.py` заново.

## Публикация на GitHub Pages

### Шаг 1 — создать репозиторий
```
git init
git add .
git commit -m "Первая версия сайта"
git branch -M main
git remote add origin https://github.com/<ваш-логин>/<название-репозитория>.git
git push -u origin main
```

### Шаг 2 — автосборка (уже настроена)
В `.github/workflows/deploy.yml` лежит GitHub Actions workflow: при каждом
`git push` в ветку `main` он сам устанавливает Python, запускает
`build.py` и публикует содержимое `docs/` в ветку `gh-pages`.

### Шаг 3 — включить Pages в настройках репозитория
GitHub → ваш репозиторий → **Settings → Pages** → в поле "Source"
выберите ветку **gh-pages** (появится после первого прогона Actions) и
папку `/ (root)`. Через минуту сайт будет доступен по адресу
`https://<ваш-логин>.github.io/<название-репозитория>/`.

Если не хотите использовать Actions — можно собирать сайт вручную
(`python build.py`), коммитить папку `docs/` вместе с остальным кодом и
в настройках Pages указать источник "**main branch /docs folder**".

## Подключение ИИ-агента

Ваше Flet-приложение (`ai-backend/flet_app.py`) развёрнуто как отдельный
веб-сервис и встраивается на сайт через `<iframe>` — выглядит и
работает так же, как и само приложение. Инструкция по деплою — в
`ai-backend/README.md`.

Файл `static/js/ai_agent.js` уже содержит готовый виджет, осталось
вписать адрес после деплоя:

```js
const AI_AGENT_CONFIG = {
  endpoint: 'https://ваш-сервис.onrender.com',
};
```

Ключ API Yandex Cloud хранится только в переменных окружения сервиса
на Render — в коде сайта и в GitHub его быть не должно.

## Структура проекта
```
university-site/
├── .github/workflows/deploy.yml
├── data/
│   ├── events.json
│   └── schedule.json
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── calendar.html
│   └── schedule.html
├── static/
│   ├── css/style.css
│   └── js/
│       ├── calendar-data.js
│       ├── calendar.js
│       ├── schedule.js
│       └── ai_agent.js
├── build.py
├── add_event.py
├── requirements.txt
└── README.md
```
