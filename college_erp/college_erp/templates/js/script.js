document.addEventListener('DOMContentLoaded', () => {
    // Current Date Display
    document.getElementById('date-display').innerText = new Date().toDateString();

    // Chart Skeleton (Data will be injected from Django later)
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Sem 1', 'Sem 2', 'Sem 3'],
            datasets: [{
                label: 'Performance',
                data: [0, 0, 0], // Start with zero/null for backend sync
                backgroundColor: '#4e73df'
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
});