let currentPage = 1;
const pageSize = 10;

// Async function to fetch data from API
async function fetchData(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching data from ${url}:`, error);
        throw error;
    }
}

// Function to update urgent tasks metric
async function updateUrgentTasksMetric() {
    try {
        const data = await fetchData('/api/urgent-tasks-report');
        document.getElementById('urgentTasksMetric').innerText = data.length;
    } catch (error) {
        console.error('Failed to update urgent tasks metric:', error);
    }
}

// Function to create tasks due chart
async function createTasksDueChart() {
    try {
        const data = await fetchData('/api/tasks-due-report');
        const taskCounts = {};
        data.forEach(task => {
            const date = new Date(task.due_by).toLocaleDateString();
            taskCounts[date] = (taskCounts[date] || 0) + 1;
        });

        const dates = Object.keys(taskCounts).sort((a, b) => new Date(a) - new Date(b));
        const counts = dates.map(date => taskCounts[date]);

        const ctx = document.getElementById('tasksDueLineChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [
                    {
                        type: 'line',
                        label: 'Tasks Due (Line)',
                        data: counts,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false,
                        yAxisID: 'y',
                    },
                    {
                        type: 'bar',
                        label: 'Tasks Due (Bar)',
                        data: counts,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y',
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Tasks'
                        },
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Failed to create tasks due chart:', error);
    }
}

// Function to create priority pie chart
async function createPriorityPieChart() {
    try {
        const data = await fetchData('/api/tasks-priority-due');
        const priorityCounts = {1: 0, 2: 0, 3: 0};
        data.forEach(task => {
            if (task.priority >= 1 && task.priority <= 3) {
                priorityCounts[task.priority]++;
            }
        });

        const priorities = Object.keys(priorityCounts);
        const counts = priorities.map(priority => priorityCounts[priority]);

        const ctx = document.getElementById('tasksPriorityPieChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Low Priority', 'Medium Priority', 'High Priority'],
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(255, 99, 132, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Task Priority Distribution'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Failed to create priority pie chart:', error);
    }
}

// Function to populate tasks table with pagination
async function populateTasksTable(page = 1) {
    try {
        const data = await fetchData(`/api/all-tasks-report?page=${page}&page_size=${pageSize}`);
        const tableBody = document.getElementById('tasksTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear existing rows
        data.tasks.forEach(task => {
            const row = tableBody.insertRow();
            row.insertCell(0).innerText = task.email;
            row.insertCell(1).innerText = task.task;
            row.insertCell(2).innerText = new Date(task.due_by).toLocaleString();
            row.insertCell(3).innerText = task.priority;
            row.insertCell(4).innerText = task.is_urgent ? 'Yes' : 'No';
        });

        // Update pagination info
        document.getElementById('pageInfoTop').innerText = `Page ${data.current_page} of ${data.total_pages}`;
        document.getElementById('pageInfoBottom').innerText = `Page ${data.current_page} of ${data.total_pages}`;
        document.getElementById('prevPageTop').disabled = data.current_page === 1;
        document.getElementById('nextPageTop').disabled = data.current_page === data.total_pages;
        document.getElementById('prevPageBottom').disabled = data.current_page === 1;
        document.getElementById('nextPageBottom').disabled = data.current_page === data.total_pages;
    } catch (error) {
        console.error('Failed to populate tasks table:', error);
    }
}

// Function to change page
function changePage(delta) {
    currentPage += delta;
    populateTasksTable(currentPage);
}

// Main function to initialize the dashboard
async function initializeDashboard() {
    try {
        await Promise.all([
            updateUrgentTasksMetric(),
            createTasksDueChart(),
            createPriorityPieChart(),
            populateTasksTable(currentPage)
        ]);
        console.log('Dashboard initialized successfully');
    } catch (error) {
        console.error('Failed to initialize dashboard:', error);
    }
}

// Call the main function to initialize the dashboard
initializeDashboard();