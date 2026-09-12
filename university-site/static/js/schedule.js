(function () {
  const tabs = document.querySelectorAll('.day-tab');
  const tables = document.querySelectorAll('.day-table');
  const groupFilter = document.getElementById('group-filter');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const day = tab.dataset.day;
      tables.forEach(table => {
        table.classList.toggle('hidden', table.dataset.day !== day);
      });
    });
  });

  groupFilter.addEventListener('change', () => {
    const value = groupFilter.value;
    document.querySelectorAll('.schedule-table tbody tr').forEach(row => {
      const match = value === 'all' || row.dataset.group === value;
      row.style.display = match ? '' : 'none';
    });
  });
})();
