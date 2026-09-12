// Виджет ИИ-агента.
// Обращается к вашему бэкенду (папка ai-backend), который безопасно хранит
// ключ Yandex Cloud и пересылает вопрос в YandexGPT. Впишите сюда адрес
// бэкенда после деплоя (см. ai-backend/README.md), например:
// endpoint: 'https://uusb-ai-backend.onrender.com/api/chat'
const AI_AGENT_CONFIG = {
  endpoint: 'https://shortkhak.onrender.com/api/chat',
};

(function () {
  const root = document.getElementById('ai-agent-root');
  if (!root) return;

  const button = document.createElement('button');
  button.className = 'ai-widget-button';
  button.textContent = '💬';
  button.setAttribute('aria-label', 'Открыть помощника');

  const panel = document.createElement('div');
  panel.className = 'ai-widget-panel';
  panel.innerHTML = `
    <strong>Помощник университета</strong>
    <div id="ai-messages" style="flex:1; overflow-y:auto; max-height:200px;"></div>
    <form id="ai-form" style="display:flex; gap:6px;">
      <input id="ai-input" type="text" placeholder="Спросите что-нибудь…" style="flex:1; padding:6px 8px; border:1px solid var(--line); border-radius:4px;">
      <button class="btn btn-primary btn-small" type="submit">→</button>
    </form>
    <p class="note">${AI_AGENT_CONFIG.endpoint ? '' : 'ИИ-агент пока не подключён к бэкенду.'}</p>
  `;

  root.appendChild(button);
  root.appendChild(panel);

  button.addEventListener('click', () => panel.classList.toggle('open'));

  panel.querySelector('#ai-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = panel.querySelector('#ai-input');
    const messages = panel.querySelector('#ai-messages');
    const text = input.value.trim();
    if (!text) return;

    messages.innerHTML += `<p><strong>Вы:</strong> ${text}</p>`;
    input.value = '';

    if (!AI_AGENT_CONFIG.endpoint) {
      messages.innerHTML += `<p><em>Агент пока не подключён. Впишите endpoint в static/js/ai_agent.js.</em></p>`;
      messages.scrollTop = messages.scrollHeight;
      return;
    }

    messages.innerHTML += `<p><em>Думаю…</em></p>`;
    messages.scrollTop = messages.scrollHeight;

    try {
      const res = await fetch(AI_AGENT_CONFIG.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      messages.innerHTML += `<p><strong>Агент:</strong> ${data.reply || 'Ответ не получен.'}</p>`;
    } catch (err) {
      messages.innerHTML += `<p><em>Не удалось связаться с сервером агента. Если бэкенд на бесплатном тарифе только что «проснулся» — попробуйте ещё раз через минуту.</em></p>`;
    }
    messages.scrollTop = messages.scrollHeight;
  });
})();
