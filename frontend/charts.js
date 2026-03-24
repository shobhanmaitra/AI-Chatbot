/**
 * Charts.js - Data Visualization Functions
 * Uses Chart.js library for beautiful charts
 */

const API_URL = 'http://localhost:5000';

// Chart instances (to destroy before creating new ones)
let currentChart = null;

/**
 * Destroy existing chart before creating new one
 */
function destroyCurrentChart() {
    if (currentChart) {
        currentChart.destroy();
        currentChart = null;
    }
}

/**
 * Show Hotel Price Comparison Bar Chart
 */
async function showHotelPricesChart() {
    try {
        const response = await fetch(`${API_URL}/api/chart/hotel-prices`);
        const data = await response.json();
        
        destroyCurrentChart();
        
        const ctx = document.getElementById('chartCanvas').getContext('2d');
        
        currentChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Average Hotel Price (₹/night)',
                    data: data.prices,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(199, 199, 199, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '🏨 Average Hotel Prices by City',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value;
                            }
                        }
                    }
                }
            }
        });
        
        showChartContainer();
        
    } catch (error) {
        console.error('Chart error:', error);
    }
}

/**
 * Show Destination Ratings Pie Chart
 */
async function showDestinationRatingsChart() {
    try {
        const response = await fetch(`${API_URL}/api/chart/destination-ratings`);
        const data = await response.json();
        
        destroyCurrentChart();
        
        const ctx = document.getElementById('chartCanvas').getContext('2d');
        
        currentChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Rating',
                    data: data.ratings,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(201, 203, 207, 0.8)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '⭐ Destination Ratings',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
        showChartContainer();
        
    } catch (error) {
        console.error('Chart error:', error);
    }
}

/**
 * Show Attraction Prices Horizontal Bar Chart
 */
async function showAttractionPricesChart() {
    try {
        const response = await fetch(`${API_URL}/api/chart/attraction-prices`);
        const data = await response.json();
        
        destroyCurrentChart();
        
        const ctx = document.getElementById('chartCanvas').getContext('2d');
        
        currentChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Entry Fee (₹)',
                    data: data.fees,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y', // Horizontal bars
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '🎫 Top Paid Attractions',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: { display: false }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value;
                            }
                        }
                    }
                }
            }
        });
        
        showChartContainer();
        
    } catch (error) {
        console.error('Chart error:', error);
    }
}

/**
 * Show Package Prices Doughnut Chart
 */
async function showPackagePricesChart() {
    try {
        const response = await fetch(`${API_URL}/api/chart/package-prices`);
        const data = await response.json();
        
        destroyCurrentChart();
        
        const ctx = document.getElementById('chartCanvas').getContext('2d');
        
        currentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Package Price (₹)',
                    data: data.prices,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(201, 203, 207, 0.8)',
                        'rgba(83, 102, 255, 0.8)',
                        'rgba(255, 99, 255, 0.8)',
                        'rgba(99, 255, 132, 0.8)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '📦 Tour Package Prices',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 15,
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
        
        showChartContainer();
        
    } catch (error) {
        console.error('Chart error:', error);
    }
}

/**
 * Show chart container
 */
function showChartContainer() {
    const container = document.getElementById('chartContainer');
    if (container) {
        container.style.display = 'block';
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * Hide chart container
 */
function hideChartContainer() {
    const container = document.getElementById('chartContainer');
    if (container) {
        container.style.display = 'none';
    }
    destroyCurrentChart();
}

/**
 * Auto-show chart based on context
 */
function autoShowChart(chartType) {
    switch(chartType) {
        case 'hotel-prices':
            showHotelPricesChart();
            break;
        case 'destination-ratings':
            showDestinationRatingsChart();
            break;
        case 'attraction-prices':
            showAttractionPricesChart();
            break;
        case 'package-prices':
            showPackagePricesChart();
            break;
        default:
            hideChartContainer();
    }
}