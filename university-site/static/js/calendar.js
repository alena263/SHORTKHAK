(function () {
  const MONTHS = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'];
  const grid = document.getElementById('calendar-grid');
  const title = document.getElementById('calendar-title');
  const dayTitle = document.getElementById('day-panel-title');
  const dayEventsEl = document.getElementById('day-events');
  const form = document.getElementById('add-event-form');

  let current = new Date();
  current.setDate(1);
  let selectedDate = toISODate(new Date());
  let events = [];

  function toISODate(d) {
    return d.toISOString().slice(0, 10);
  }

  async function refresh() {
    events = await loadEvents();
    render();
  }

  function render() {
    title.textContent = `${MONTHS[current.getMonth()]} ${current.getFullYear()}`;
    grid.innerHTML = '';

    const year = current.getFullYear();
    const month = current.getMonth();
    const firstDay = new Date(year, month, 1);
    // Понедельник = 0
    const startOffset = (firstDay.getDay() + 6) % 7;
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    const todayISO = toISODate(new Date());

    const cells = [];
    for (let i = startOffset; i > 0; i--) {
      cells.push({ day: daysInPrevMonth - i + 1, outside: true, month: month - 1 });
    }
    for (let d = 1; d <= daysInMonth; d++) {
      cells.push({ day: d, outside: false, month });
    }
    while (cells.length % 7 !== 0) {
      cells.push({ day: cells.length - (startOffset + daysInMonth) + 1, outside: true, month: month + 1 });
    }

    cells.forEach(cell => {
      const cellDate = new Date(year, cell.month, cell.day);
      const iso = toISODate(cellDate);
      const el = document.createElement('div');
      el.className = 'cal-day';
      if (cell.outside) el.classList.add('outside');
      if (iso === todayISO) el.classList.add('today');
      if (iso === selectedDate) el.classList.add('selected');

      const hasEvent = events.some(e => e.date === iso);
      el.innerHTML = `<span>${cell.day}</span>` + (hasEvent ? '<span class="dot"></span>' : '');
      el.addEventListener('click', () => {
        selectedDate = iso;
        if (cell.outside) {
          current = new Date(year, cell.month, 1);
        }
        render();
      });
      grid.appendChild(el);
    });

    renderDayPanel();
  }

  function renderDayPanel() {
    const d = new Date(selectedDate + 'T00:00:00');
    dayTitle.textContent = d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
    const dayEvents = events.filter(e => e.date === selectedDate);
    dayEventsEl.innerHTML = '';
    if (dayEvents.length === 0) {
      dayEventsEl.innerHTML = '<li class="muted">На этот день мероприятий нет.</li>';
      return;
    }
    dayEvents.forEach(e => {
      const li = document.createElement('li');
      li.innerHTML = `<div>
        <strong>${e.title}</strong>${e.time ? ' · ' + e.time : ''}<br>
        <span class="muted">${e.location || ''}</span><br>
        <span class="muted">${e.description || ''}</span>
      </div>`;
      dayEventsEl.appendChild(li);
    });
  }

  document.getElementById('prev-month').addEventListener('click', () => {
    current.setMonth(current.getMonth() - 1);
    render();
  });
  document.getElementById('next-month').addEventListener('click', () => {
    current.setMonth(current.getMonth() + 1);
    render();
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const newEvent = {
      title: data.get('title'),
      date: data.get('date'),
      time: data.get('time'),
      location: data.get('location'),
      description: data.get('description')
    };
    addLocalEvent(newEvent);
    selectedDate = newEvent.date;
    current = new Date(newEvent.date + 'T00:00:00');
    current.setDate(1);
    form.reset();
    refresh();
  });

  refresh();
})();
