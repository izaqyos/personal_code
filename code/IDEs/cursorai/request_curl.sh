#!/bin/bash

# Create a new todo and capture the ID
response=$(curl -X POST -H "Content-Type: application/json" -d '{"task": "Buy groceries"}' http://localhost:3000/todos)
todo_id=$(echo "$response" | jq -r '.id')  # Requires 'jq' to be installed

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq is not installed. Please install it:  brew install jq (or use your package manager)"
    exit 1
fi


if [ -z "$todo_id" ]; then
  echo "Error: Could not create todo or extract ID."
  exit 1
fi

echo "Created todo with ID: $todo_id"

# Get all todos
echo "Getting all todos:"
curl http://localhost:3000/todos

# Get the specific todo
echo "Getting todo with ID $todo_id:"
curl "http://localhost:3000/todos/$todo_id"

# Update the todo
echo "Updating todo with ID $todo_id:"
response=$(curl -X PUT -H "Content-Type: application/json" -d '{"task": "Buy milk and eggs", "completed": true}' "http://localhost:3000/todos/$todo_id")
echo "$response"

# Get all todos again (to see the update)
echo "Getting all todos (after update):"
curl http://localhost:3000/todos

# Delete the todo
echo "Deleting todo with ID $todo_id:"
curl -X DELETE "http://localhost:3000/todos/$todo_id"

# Get all todos again (should be empty)
echo "Getting all todos (after delete):"
curl http://localhost:3000/todos

echo "Done."