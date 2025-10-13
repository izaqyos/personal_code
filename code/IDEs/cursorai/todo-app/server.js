// server.js
const express = require('express');
const { v4: uuidv4 } = require('uuid');
const Todo = require('./models/todo');

const app = express();
const port = 3000;

app.use(express.json()); // Middleware to parse JSON request bodies

// In-memory storage for our ToDo items (replace with a database in a real app)
let todos = [];

// --- API Routes ---

// GET all todos
app.get('/todos', (req, res) => {
    res.json(todos);
});

// GET a single todo by ID
app.get('/todos/:id', (req, res) => {
    const id = req.params.id;
    const todo = todos.find(todo => todo.id === id);
    if (!todo) {
        return res.status(404).json({ message: 'Todo not found' });
    }
    res.json(todo);
});

// POST (create) a new todo
app.post('/todos', (req, res) => {
    if (!Todo.validate(req.body)) {
        return res.status(400).json({ message: 'Invalid todo data' });
    }

    const newTodo = new Todo(uuidv4(), req.body.task, req.body.completed || false);
    todos.push(newTodo);
    res.status(201).json(newTodo); // 201 Created
});

// PUT (update) an existing todo
app.put('/todos/:id', (req, res) => {
    const id = req.params.id;
    const todoIndex = todos.findIndex(todo => todo.id === id);

    if (todoIndex === -1) {
        return res.status(404).json({ message: 'Todo not found' });
    }
    if (!Todo.validate(req.body)) {
        return res.status(400).json({ message: 'Invalid todo data' });
    }

    todos[todoIndex] = {
      ...todos[todoIndex],
      task: req.body.task,
      completed: req.body.completed !== undefined ? req.body.completed : todos[todoIndex].completed
    }

    res.json(todos[todoIndex]);
});

// DELETE a todo
app.delete('/todos/:id', (req, res) => {
    const id = req.params.id;
    const todoIndex = todos.findIndex(todo => todo.id === id);

    if (todoIndex === -1) {
        return res.status(404).json({ message: 'Todo not found' });
    }

    todos.splice(todoIndex, 1); // Remove the todo
    res.status(204).send(); // 204 No Content (successful deletion)
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});