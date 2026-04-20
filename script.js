Here's the complete `script.js` for a To-Do List application with all the requested functionalities:

```javascript
// DOM Elements
const taskInput = document.getElementById('task-input');
const addTaskBtn = document.getElementById('add-task-btn');
const taskList = document.getElementById('task-list');
const filterAll = document.getElementById('filter-all');
const filterActive = document.getElementById('filter-active');
const filterCompleted = document.getElementById('filter-completed');
const clearCompletedBtn = document.getElementById('clear-completed');

// Initialize tasks array
let tasks = [];

// Event Listeners
document.addEventListener('DOMContentLoaded', loadTasks);
addTaskBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTask();
    }
});
filterAll.addEventListener('click', () => filterTasks('all'));
filterActive.addEventListener('click', () => filterTasks('active'));
filterCompleted.addEventListener('click', () => filterTasks('completed'));
clearCompletedBtn.addEventListener('click', clearCompletedTasks);

// Load tasks from localStorage
function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
        renderTasks();
    }
}

// Save tasks to localStorage
function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Add a new task
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText) {
        const newTask = {
            id: Date.now(),
            text: taskText,
            completed: false
        };
        tasks.push(newTask);
        saveTasks();
        renderTasks();
        taskInput.value = '';
    }
}

// Render tasks based on current filter
function renderTasks(filter = 'all') {
    taskList.innerHTML = '';
    
    let filteredTasks = tasks;
    if (filter === 'active') {
        filteredTasks = tasks.filter(task => !task.completed);
    } else if (filter === 'completed') {
        filteredTasks = tasks.filter(task => task.completed);
    }
    
    if (filteredTasks.length === 0) {
        taskList.innerHTML = '<p class="empty-message">No tasks found</p>';
        return;
    }
    
    filteredTasks.forEach(task => {
        const taskItem = document.createElement('li');
        taskItem.className = 'task-item';
        if (task.completed) {
            taskItem.classList.add('completed');
        }
        
        taskItem.innerHTML = `
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}">
            <span class="task-text">${task.text}</span>
            <button class="delete-btn" data-id="${task.id}">×</button>
        `;
        
        taskList.appendChild(taskItem);
    });
    
    // Add event listeners to new elements
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', toggleTask);
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', deleteTask);
    });
}

// Toggle task completion status
function toggleTask(e) {
    const taskId = parseInt(e.target.dataset.id);
    const task = tasks.find(task => task.id === taskId);
    if (task) {
        task.completed = e.target.checked;
        saveTasks();
        renderTasks();
    }
}

// Delete a task
function deleteTask(e) {
    const taskId = parseInt(e.target.dataset.id);
    tasks = tasks.filter(task => task.id !== taskId);
    saveTasks();
    renderTasks();
}

// Filter tasks
function filterTasks(filter) {
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderTasks(filter);
}

// Clear all completed tasks
function clearCompletedTasks() {
    tasks = tasks.filter(task => !task.completed);
    saveTasks();
    renderTasks();
}
```

This JavaScript code provides the following functionality:

1. **Task Management**:
   - Add new tasks (either by button click or pressing Enter)
   - Toggle task completion status
   - Delete individual tasks
   - Clear all completed tasks at once

2. **Task Filtering**:
   - Show all tasks
   - Show only active tasks
   - Show only completed tasks

3. **Persistence**:
   - Tasks are saved to localStorage so they persist between page reloads

4. **UI Updates**:
   - Proper rendering of tasks based on current filter
   - Visual feedback for completed tasks
   - Active filter button highlighting

The code is organized with clear functions for each operation and includes event listeners for all user interactions. It follows modern JavaScript best practices and maintains a clean separation of concerns.

To use this, you'll need to pair it with appropriate HTML and CSS, and ensure the element IDs match those used in the JavaScript code. The code assumes you have the following HTML elements:
- A text input with id "task-input"
- A button with id "add-task-btn"
- A ul element with id "task-list"
- Filter buttons with ids "filter-all", "filter-active", and "filter-completed"
- A clear completed button with id "clear-completed"