#!/bin/bash

# Create the project directory
mkdir todo-app

# Change into the project directory
cd todo-app

# Create the models directory
mkdir models

# Create the empty files
touch package.json
touch server.js
touch models/todo.js

# (Optional) Initialize a git repository
git init

echo "Project skeleton created! Now run:"
echo "  cd todo-app"
echo "  # (Paste the contents of package.json into the file)"
echo "  # (Paste the contents of server.js into the file)"
echo "  # (Paste the contents of models/todo.js into the file)"
echo "  npm install"
echo "  npm start"
