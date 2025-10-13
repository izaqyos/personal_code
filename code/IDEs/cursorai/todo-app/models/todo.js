// models/todo.js

class Todo {
    constructor(id, task, completed = false) {
        this.id = id;
        this.task = task;
        this.completed = completed;
    }

    // Example method (you could add more)
    static validate(todoData) {
        if (!todoData || !todoData.task || typeof todoData.task !== 'string' || todoData.task.trim() === '') {
            return false; // Invalid
        }
        return true; // Valid
    }
}

module.exports = Todo;