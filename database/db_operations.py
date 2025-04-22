import sqlite3


def check_user_credentials(login, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE login = ? AND password = ?", (login, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_box_types():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT type_name FROM box_types")
    box_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return box_types


def get_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product_name FROM products")
    products = [row[0] for row in cursor.fetchall()]
    conn.close()
    return products


def save_box_data(
    packaging_company, export_company, box_type, width, height, product, box_count
):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Quti turini ID sifatida olish
    cursor.execute("SELECT id FROM box_types WHERE type_name = ?", (box_type,))
    box_type_id = cursor.fetchone()[0]

    # Mahsulot turini ID sifatida olish
    cursor.execute("SELECT id FROM products WHERE product_name = ?", (product,))
    product_id = cursor.fetchone()[0]

    # Boxes jadvaliga saqlash
    cursor.execute(
        """
        INSERT INTO boxes (packaging_company, export_company, box_type_id, width, height, product_id, box_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            packaging_company,
            export_company,
            box_type_id,
            width,
            height,
            product_id,
            box_count,
        ),
    )
    box_id = cursor.lastrowid

    conn.commit()
    return conn, cursor, box_id


def save_datamatrix_code(conn, cursor, box_id, unique_id):
    cursor.execute(
        "INSERT INTO datamatrix_codes (box_id, unique_id) VALUES (?, ?)",
        (box_id, unique_id),
    )
    conn.commit()
