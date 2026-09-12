
const LOCAL_EVENTS_KEY = 'university_local_events';

async function loadEvents() {
  let baseEvents = [];
  try {
    const res = await fetch('data/events.json');
    baseEvents = await res.json();
  } catch (err) {
    console.warn('Не удалось загрузить data/events.json', err);
  }
  const local = getLocalEvents();
  return [...baseEvents, ...local];
}

function getLocalEvents() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_EVENTS_KEY)) || [];
  } catch {
    return [];
  }
}

function addLocalEvent(event) {
  const events = getLocalEvents();
  event.id = 'local-' + Date.now();
  events.push(event);
  localStorage.setItem(LOCAL_EVENTS_KEY, JSON.stringify(events));
  return event;
}
