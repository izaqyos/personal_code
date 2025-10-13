# ToDo List Backend

This is a simple backend application for managing a ToDo list, built using Node.js and Express. The application provides a RESTful API to perform CRUD operations on ToDo items.

## Features

- **Create** a new ToDo item
- **Read** all ToDo items or a single item by ID
- **Update** an existing ToDo item
- **Delete** a ToDo item

## Technologies Used

- Node.js
- Express
- UUID for generating unique identifiers
- PostgreSQL (planned for future implementation)

## Project Structure

- `server.js`: Main server file that sets up the Express application and defines API routes.
  ```javascript:server.js
  startLine: 2
  endLine: 78
  ```

- `models/todo.js`: Defines the `Todo` class and includes a static method for validating ToDo data.
  ```javascript:models/todo.js
  startLine: 3
  endLine: 19
  ```

- `package.json`: Contains project metadata and dependencies.
  ```json:package.json
  startLine: 1
  endLine: 16
  ```

- `tests.js`: Placeholder for test cases to ensure the application functions correctly.
  ```javascript:tests.js
  startLine: 1
  endLine: 1
  ```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the application**:
   ```bash
   npm start
   ```

   The server will start on `http://localhost:3000`.

## API Endpoints

- **GET /todos**: Retrieve all ToDo items.
- **GET /todos/:id**: Retrieve a single ToDo item by ID.
- **POST /todos**: Create a new ToDo item.
- **PUT /todos/:id**: Update an existing ToDo item by ID.
- **DELETE /todos/:id**: Delete a ToDo item by ID.

## Testing

Tests are planned to be implemented using Mocha and Chai. The `tests.js` file will contain test cases for the API endpoints.

## Future Improvements

- Integrate PostgreSQL for persistent data storage.
- Implement comprehensive test cases.
- Add user authentication and authorization.

## License

This project is licensed under the ISC License.