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

## Подключение ИИ-агента (на будущее)

Файл `static/js/ai_agent.js` уже содержит виджет-чат и точку подключения:

```js
const AI_AGENT_CONFIG = {
  enabled: false,
  endpoint: '', // адрес вашего бэкенда
};
```

Важно: GitHub Pages — статичный хостинг, поэтому ключ API (например, для
Anthropic Claude) нельзя хранить в JS-коде — он будет виден каждому
посетителю. Когда будете готовы подключить агента:

1. Разверните небольшой бэкенд отдельно (Flask/FastAPI на Render,
   Railway, Vercel Functions, Cloudflare Workers и т.п.), который
   принимает `POST { message }` и обращается к API модели, используя
   ключ, хранящийся в переменных окружения сервера, а не в браузере.
2. Впишите адрес этого бэкенда в `endpoint` и поставьте `enabled: true`.
3. Виджет на сайте заработает без дополнительных правок фронтенда.

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
