# TodoApp with FastAPI

A Todo application built with FastAPI, demonstrating CRUD operations, authentication, and full-stack development.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete todos.
- **Authentication**: Secure your API with JSON Web Tokens (JWT).
- **Database**: Use MySQL for persistent storage.
- **Testing**: Includes unit and integration tests.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/mukhtar-ahmed/todo-fastapi.git
    cd todo-fastapi
    ```

2. **Setup Environment**

    ```bash
    poetry install
    ```

3. **Run the Application**

    ```bash
    poetry run uvicorn app.main:app --reload
    ```

## Usage

Access the API at `http://127.0.0.1:8000`. The API documentation is available at `http://127.0.0.1:8000/docs`.

## Contributing

Feel free to open issues or submit pull requests to contribute to the project.
