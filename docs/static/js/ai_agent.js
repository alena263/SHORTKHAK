// Виджет ИИ-агента: встраивает ваше Flet-приложение (папка ai-backend)
// через iframe — на сайте оно выглядит и работает так же, как и само
// приложение. Впишите сюда адрес после деплоя (см. ai-backend/README.md),
// например: endpoint: 'https://uusb-ai-agent.onrender.com'
const AI_AGENT_CONFIG = {
  endpoint: 'https://shortkhak-2.onrender.com/',
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

  if (AI_AGENT_CONFIG.endpoint) {
    panel.innerHTML = `
      <div class="ai-widget-header">
        <strong>Помощник университета</strong>
        <button class="ai-widget-close" aria-label="Закрыть">×</button>
      </div>
      <iframe class="ai-widget-frame" src="${AI_AGENT_CONFIG.endpoint}" title="ИИ-агент"></iframe>
    `;
  } else {
    panel.innerHTML = `
      <div class="ai-widget-header">
        <strong>Помощник университета</strong>
        <button class="ai-widget-close" aria-label="Закрыть">×</button>
      </div>
      <p class="note">ИИ-агент пока не подключён. Впишите endpoint в static/js/ai_agent.js.</p>
    `;
  }

  root.appendChild(button);
  root.appendChild(panel);

  button.addEventListener('click', () => panel.classList.toggle('open'));
  panel.querySelector('.ai-widget-close').addEventListener('click', () => panel.classList.remove('open'));
})();
