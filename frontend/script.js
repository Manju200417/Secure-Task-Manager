const API_URL = 'http://localhost:5000/api/v1';

/* =========================
   AUTH CHECK
========================= */
function checkAuth() {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname;

    if (!token && currentPage.includes('dashboard')) {
        window.location.href = 'index.html';
    }

    if (token && currentPage.includes('index')) {
        window.location.href = 'dashboard.html';
    }
}

/* =========================
   REGISTER
========================= */
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const role = document.getElementById('reg-role').value;

        try {
            const res = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password, role })
            });

            const data = await res.json();

            const msg = document.getElementById('register-message');
            if (res.ok) {
                msg.textContent = 'Registration successful. Please login.';
                msg.style.color = 'green';
                registerForm.reset();
            } else {
                msg.textContent = data.error || 'Registration failed';
                msg.style.color = 'red';
            }
        } catch {
            document.getElementById('register-message').textContent = 'Server error';
        }
    });
}

/* =========================
   LOGIN
========================= */
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            const res = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                document.getElementById('login-message').textContent = data.error;
            }
        } catch {
            document.getElementById('login-message').textContent = 'Server error';
        }
    });
}

/* =========================
   DASHBOARD INIT
========================= */
if (document.getElementById('tasks-list')) {
    const user = JSON.parse(localStorage.getItem('user'));
    document.getElementById('user-info').textContent =
        `Welcome, ${user.name} (${user.role})`;

    if (user.role === 'admin') {
        document.getElementById('admin-section').style.display = 'block';
        loadAllUsers();
    }

    loadTasks();
}

/* =========================
   CREATE TASK
========================= */
const taskForm = document.getElementById('taskForm');
if (taskForm) {
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('task-title').value;
        const description = document.getElementById('task-description').value;
        const token = localStorage.getItem('token');

        try {
            const res = await fetch(`${API_URL}/tasks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title, description })
            });

            if (res.ok) {
                taskForm.reset();
                loadTasks();
            } else {
                alert('Failed to create task');
            }
        } catch {
            alert('Server error');
        }
    });
}

/* =========================
   LOAD TASKS
========================= */
async function loadTasks() {
    const token = localStorage.getItem('token');

    const res = await fetch(`${API_URL}/tasks`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const data = await res.json();
    if (res.ok) displayTasks(data.tasks);
}

/* =========================
   DISPLAY TASKS (FIXED)
========================= */
function displayTasks(tasks) {
    const container = document.getElementById('tasks-list');
    container.innerHTML = '';

    if (!tasks || tasks.length === 0) {
        container.innerHTML = '<p>No tasks found.</p>';
        return;
    }

    tasks.forEach(task => {
        const div = document.createElement('div');
        div.className = 'task-item';
        div.style.cursor = 'pointer';

        div.innerHTML = `
            <h3>${task.title}</h3>
            <p>${task.description || ''}</p>
            <small>User ID: ${task.user_id}</small><br>
            <button>Delete</button>
       `;

        // CLICK TASK → SHOW DETAILS
        div.onclick = () => {
            alert(
                `Task Details\n\nTitle: ${task.title}\nDescription: ${task.description || 'None'}`
            );
        };

        // DELETE BUTTON
        const deleteBtn = div.querySelector('button');
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            deleteTask(task.id);
        };

        container.appendChild(div);
    });
}

/* =========================
   DELETE TASK
========================= */
async function deleteTask(taskId) {
    const token = localStorage.getItem('token');

    if (!confirm('Delete this task?')) return;

    const res = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.ok) loadTasks();
    else alert('Failed to delete task');
}

/* =========================
   ADMIN: LOAD USERS
========================= */
async function loadAllUsers() {
    const token = localStorage.getItem('token');

    const res = await fetch(`${API_URL}/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const data = await res.json();
    if (res.ok) displayUsers(data.users);
}

function displayUsers(users) {
    const container = document.getElementById('users-list');
    container.innerHTML = '';

    users.forEach(user => {
        const div = document.createElement('div');
        div.innerHTML = `
            <p>${user.name} (${user.role})</p>
            <button onclick="deleteUser(${user.id})">Delete</button>
        `;
        container.appendChild(div);
    });
}

async function deleteUser(userId) {
    const token = localStorage.getItem('token');

    if (!confirm('Delete user?')) return;

    const res = await fetch(`${API_URL}/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.ok) loadAllUsers();
}

/* =========================
   LOGOUT
========================= */
function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

checkAuth();
