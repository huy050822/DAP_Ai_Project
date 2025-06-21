document.addEventListener('DOMContentLoaded', function() {
    // Get theme toggle button
    const themeToggle = document.querySelector('.theme-toggle');
    
    // Function to update chart colors based on theme
    function updateChartColors() {
        const isDark = document.body.classList.contains('dark-mode');
        const theme = {
            text: isDark ? '#ffffff' : '#333333',
            grid: isDark ? '#404040' : '#e0e0e0',
            revenue: {
                border: 'rgb(221, 107, 32)',
                background: isDark ? 'rgba(221, 107, 32, 0.2)' : 'rgba(221, 107, 32, 0.1)'
            },
            orders: {
                border: 'rgb(75, 192, 192)',
                background: isDark ? 'rgba(75, 192, 192, 0.2)' : 'rgba(75, 192, 192, 0.1)'
            }
        };

        // Update revenue chart if it exists
        const revenueChart = Chart.getChart('revenueChart');
        if (revenueChart) {
            // Update datasets colors
            revenueChart.data.datasets[0].backgroundColor = theme.revenue.background;
            revenueChart.data.datasets[1].backgroundColor = theme.orders.background;
            
            // Update chart options
            revenueChart.options.scales.y.grid.color = theme.grid;
            revenueChart.options.scales.x.grid.color = theme.grid;
            revenueChart.options.scales.y.ticks.color = theme.text;
            revenueChart.options.scales.x.ticks.color = theme.text;
            
            revenueChart.update();
        }
    }

    // Handle theme toggle click
    if (themeToggle) {
        themeToggle.addEventListener('click', (e) => {
            // Since we're using separate HTML files for themes,
            // the link itself handles the navigation
        });
    }

    // Chart initialization
    const revenueCtx = document.getElementById('revenueChart');
    if (revenueCtx) {
        const revenueChart = new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [
                    {
                        label: 'Revenue',
                        data: [9000, 15000, 12000, 17000, 18288, 21000, 27000],
                        borderColor: 'rgb(221, 107, 32)',
                        backgroundColor: 'rgba(221, 107, 32, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: 'rgb(221, 107, 32)',
                        order: 1
                    },
                    {
                        label: 'Orders',
                        data: [11000, 12000, 14000, 16000, 17000, 25000, 28000],
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: 'rgb(75, 192, 192)',
                        order: 2
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                },
                scales: {
                    x: {
                        grid: {
                            color: '#e0e0e0'
                        },
                        ticks: {
                            color: '#333333'
                        }
                    },
                    y: {
                        grid: {
                            color: '#e0e0e0'
                        },
                        ticks: {
                            color: '#333333'
                        },
                        beginAtZero: true,
                        suggestedMax: 36000
                    }
                }
            }
        });

        // Update chart colors when it's first created
        updateChartColors();

        // Orders toggle functionality
        const ordersButton = document.querySelector('.orders-btn');
        if (ordersButton) {
            ordersButton.addEventListener('click', () => {
                const ordersDataset = revenueChart.data.datasets[1];
                ordersDataset.hidden = !ordersDataset.hidden;
                revenueChart.update();
            });
        }
    }

    // Top Ads Pie Chart
    const topAdsCtx = document.getElementById('topAdsChart');
    if (topAdsCtx) {
        new Chart(topAdsCtx, {
            type: 'pie',
            data: {
                labels: [
                    'Fashion Ads campaign',
                    'Gadget Ads campaign',
                    'Books Ads campaign',
                    'Sports Ads campaign',
                    'Groceries Ads campaign'
                ],
                datasets: [{
                    data: [38600, 30800, 22500, 5000, 3100],
                    backgroundColor: [
                        '#f4c542', // Fashion
                        '#6fcf97', // Gadget
                        '#9b51e0', // Books
                        '#56ccf2', // Sports
                        '#f2994a'  // Groceries
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Mobile sidebar functionality
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });

        // Close sidebar when clicking outside
        document.addEventListener('click', (event) => {
            if (sidebar.classList.contains('open') && 
                !sidebar.contains(event.target) && 
                !menuToggle.contains(event.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
});
