async function fetchTodos() {
    const response = await fetch('/todos/todos_json');
    if (!response.ok) {
        console.error('Failed to fetch todos');
        return [];
    }
    return await response.json();
}

async function checkDueDates() {
    const todos = await fetchTodos();
    const now = new Date();
    todos.forEach(todo => {
        const dueDate = new Date(todo.due_date); // Assuming due_date is a valid date string
        if (dueDate < now) {
            alert(`Reminder: The todo "${todo.title}" is past its due date!`);
        }
    });
}

// Check for overdue todos immediately and then every 15 minutes
checkDueDates(); // Initial check
setInterval(checkDueDates, 60 * 1000 * 15); // Check every 15 minutes