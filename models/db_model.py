from db.connection import get_connection

#Function to create the necessary tables if they do not exist.
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    #Authors table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id BIGSERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id BIGSERIAL PRIMARY KEY,
            title VARCHAR(255),
            author_id INTEGER REFERENCES authors(id),
            price NUMERIC(18, 4),
            stock INTEGER DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id BIGSERIAL PRIMARY KEY,
            account_id BIGINT UNIQUE NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id BIGSERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id BIGSERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
            book_id INTEGER REFERENCES books(id),
            quantity INTEGER NOT NULL,
            unit_price NUMERIC(18, 4) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()