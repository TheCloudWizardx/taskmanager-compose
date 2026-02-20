const API_URL = '/api';

// Load tasks on page load
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadTasks();
    
    // Enter key to add task
    document.getElementById('taskInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });
});

async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        const statusEl = document.getElementById('healthStatus');
        
        if (data.status === 'healthy') {
            statusEl.textContent = '✅ Backend connected';
            statusEl.className = 'health-status healthy';
        } else {
            statusEl.textContent = '❌ Backend unhealthy';
            statusEl.className = 'health-status unhealthy';
        }
    } catch (error) {
        document.getElementById('healthStatus').textContent = '❌ Cannot connect to backend';
        document.getElementById('healthStatus').className = 'health-status unhealthy';
    }
}

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const tasks = await response.json();
        
        renderTasks(tasks);
        updateStats(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
        document.getElementById('taskList').innerHTML = 
            '<div class="empty-state">❌ Error loading tasks</div>';
    }
}

function renderTasks(tasks) {
    const taskList = document.getElementById('taskList');
    
    if (tasks.length === 0) {
        taskList.innerHTML = '<div class="empty-state">No tasks yet. Add one above!</div>';
        return;
    }
    
    taskList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <input type="checkbox" 
                   ${task.completed ? 'checked' : ''} 
                   onchange="toggleTask(${task.id}, this.checked)">
            <span>${task.title}</span>
            <button onclick="deleteTask(${task.id})">Delete</button>
        </div>
    `).join('');
}

function updateStats(tasks) {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;
    
    document.getElementById('totalTasks').textContent = total;
    document.getElementById('completedTasks').textContent = completed;
    document.getElementById('pendingTasks').textContent = pending;
}

async function addTask() {
    const input = document.getElementById('taskInput');
    const title = input.value.trim();
    
    if (!title) {
        alert('Please enter a task');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title }),
        });
        
        if (response.ok) {
            input.value = '';
            loadTasks();
        } else {
            alert('Error adding task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding task');
    }
}

async function toggleTask(id, completed) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed }),
        });
        
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function deleteTask(id) {
    if (!confirm('Delete this task?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE',
        });
        
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
