  function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    sidebar.classList.toggle('mobile-visible');
    overlay.classList.toggle('visible');
  }

  const ctx1 = document.getElementById('salesChart').getContext('2d');
  new Chart(ctx1, {
    type: 'line',
    data: {
      labels: ['Feb 28', 'Mar 31', 'Apr 30', 'May 31', 'Jun 30', 'Jul 31'],
      datasets: [{
        label: 'Sales',
        data: [85, 255, 340, 260, 200, 120],
        backgroundColor: 'rgba(0, 201, 255, 0.2)',
        borderColor: '#00c9ff',
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true },
        x: { grid: { display: false } }
      }
    }
  });

  const ctx2 = document.getElementById('lifetimeChart').getContext('2d');
  new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: ['Completed', 'Cancelled'],
      datasets: [{
        data: [0, 0],
        backgroundColor: ['#28a745', '#ff6b6b']
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      cutout: '70%'
    }
  });