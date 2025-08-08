from db.connection import get_connection

#Function to create the necessary tables if they do not exist.
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id BIGSERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS author_details (
            author_id BIGINT PRIMARY KEY REFERENCES authors(id) ON DELETE CASCADE,
            photo_url TEXT,
            overview TEXT,
            hometown VARCHAR(100),
            birthday DATE,
            website TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS author_education (
            id SERIAL PRIMARY KEY,
            author_id BIGINT REFERENCES authors(id) ON DELETE CASCADE,
            degree VARCHAR(100),
            institution VARCHAR(100),
            graduation_year SMALLINT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id BIGSERIAL PRIMARY KEY,
            cover_image_url TEXT,
            title VARCHAR(255),
            author_id BIGINT REFERENCES authors(id),
            publisher VARCHAR(100),
            ISBN VARCHAR(13),
            price NUMERIC(18, 4),
            book_format VARCHAR(50),
            stock INTEGER DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS book_details (
            book_id BIGINT PRIMARY KEY REFERENCES books(id) ON DELETE CASCADE,
            overview TEXT,
            publication_date DATE,
            page_count INTEGER,
            length_cm NUMERIC(5,2),
            width_cm NUMERIC(5,2),
            height_cm NUMERIC(5,2)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS book_genres (
            book_id INT REFERENCES books(id) ON DELETE CASCADE,
            genre_id INT REFERENCES genres(id) ON DELETE CASCADE,
            PRIMARY KEY (book_id, genre_id)
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
            order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
            book_id BIGINT REFERENCES books(id),
            quantity INTEGER NOT NULL,
            unit_price NUMERIC(18, 4) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
        id SERIAL PRIMARY KEY,
        currency_from VARCHAR(3) NOT NULL,
        currency_to VARCHAR(3) NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(currency_from, currency_to)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS discounts (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            discount_type VARCHAR(10) CHECK (discount_type IN ('fixed', 'percent')),
            value NUMERIC(18,4) NOT NULL,
            start_date DATE,
            end_date DATE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS book_discounts (
            book_id BIGINT REFERENCES books(id) ON DELETE CASCADE,
            discount_id BIGINT REFERENCES discounts(id) ON DELETE CASCADE,
            PRIMARY KEY (book_id, discount_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS genre_discounts (
            genre_id INT REFERENCES genres(id) ON DELETE CASCADE,
            discount_id BIGINT REFERENCES discounts(id) ON DELETE CASCADE,
            PRIMARY KEY (genre_id, discount_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()