# Bookstore Management System – Python & PostgreSQL

A bookstore management system built with Python and PostgreSQL. The project is structured modularly and follows standard CRUD function naming. It is designed as a practical learning tool for reinforcing Python skills and database design principles.

## Features

- Create, read, update, and delete authors
- PostgreSQL database integration using psycopg2
- Secure connection via environment variables (`.env`)
- Modular project structure for scalability and clarity
- Command-line interface (CLI)

## Technologies Used

- Python 3.11+
- PostgreSQL
- psycopg2
- python-dotenv

## Project Structure

```
Python-BookstoreApp/
├── .env                  # Contains DB credentials (excluded from version control)
├── .gitignore
├── main.py               # Entry point for the application
├── requirements.txt
│
├── config/
│   └── settings.py       # Loads environment variables
│
├── db/
│   └── connection.py     # Singleton-style DB connection
│
├── models/
│   └── db_model.py       # Table definitions (e.g., authors, books)
│
├── services/
│   └── author_service.py # CRUD functions for authors
│
├── cli/
│   └── author_cli.py     # Terminal interface for author operations
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Thazon/Python-BookstoreApp.git
cd Python-BookstoreApp
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

```
DB_NAME=bookstore
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

> Note: This file is excluded from Git to avoid exposing credentials.

### 5. Create the PostgreSQL database (if not already created)

```sql
CREATE DATABASE bookstore;
```

## Usage

### Run the application

```bash
python main.py
```

This will:

- Establish a connection to the PostgreSQL database
- Create the required tables (if they do not already exist)
- Launch the CLI interface for interacting with authors

## Author CLI Example

```bash
1. Create Author
2. View All Authors
3. View Author by ID
4. Update Author
5. Delete Author
6. Exit
```

## Author Table Schema

```sql
CREATE TABLE authors (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);
```

## Planned Features

- Book, order, customer management (CRUD)
- Orders and order items
- Reporting (CSV, PDF exports)
- Basic authentication for CLI
- Optional web interface (Flask or FastAPI)
- Unit and integration testing

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

Email: badoitiberiualexandru@gmail.com
[LinkedIn](www.linkedin.com/in/tiberiu-alexandru-badoi-b5b902224)
