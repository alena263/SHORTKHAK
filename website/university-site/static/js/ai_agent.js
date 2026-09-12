// Виджет ИИ-агента.
// GitHub Pages отдаёт только статику, поэтому напрямую вызывать Anthropic API
// с ключом из браузера нельзя (ключ окажется виден всем). Когда будет готов
// отдельный бэкенд (например, небольшое Flask/FastAPI-приложение на Render,
// Railway или Cloudflare Workers), укажите его адрес ниже — и виджет заработает.
const AI_AGENT_CONFIG = {
  enabled: false,          // поставьте true, когда подключите бэкенд
  endpoint: '',            // например: 'https://your-backend.example.com/api/chat'
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
    <p class="note">${AI_AGENT_CONFIG.enabled ? '' : 'ИИ-агент пока не подключён к бэкенду.'}</p>
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

    if (!AI_AGENT_CONFIG.enabled || !AI_AGENT_CONFIG.endpoint) {
      messages.innerHTML += `<p><em>Агент пока не подключён. Настройте AI_AGENT_CONFIG в static/js/ai_agent.js.</em></p>`;
      messages.scrollTop = messages.scrollHeight;
      return;
    }

    try {
      const res = await fetch(AI_AGENT_CONFIG.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      messages.innerHTML += `<p><strong>Агент:</strong> ${data.reply || 'Ответ не получен.'}</p>`;
    } catch (err) {
      messages.innerHTML += `<p><em>Ошибка обращения к серверу агента.</em></p>`;
    }
    messages.scrollTop = messages.scrollHeight;
  });
})();
