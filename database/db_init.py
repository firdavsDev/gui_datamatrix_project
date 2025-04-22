import sqlite3


def initialize_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Foydalanuvchilar jadvali
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (login, password) VALUES (?, ?)",
        ("admin", "admin"),
    )

    # Quti turlari jadvali
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS box_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL UNIQUE
        )
    """
    )
    box_types = ["Temir", "Karton", "Aluminiy", "Setka", "Plastmassa"]
    for box_type in box_types:
        cursor.execute(
            "INSERT OR IGNORE INTO box_types (type_name) VALUES (?)", (box_type,)
        )

    # Mahsulot turlari jadvali
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL UNIQUE
        )
    """
    )
    products = [
        "Olma",
        "Anor",
        "Pomidor",
        "Uzum",
        "Shaftoli",
        "Behi",
        "Nok",
        "Gilos",
        "Olcha",
        "Qulupnay",
        "Malina",
        "Kivi",
        "Limon",
        "Apelsin",
        "Mandarin",
        "Banan",
        "Ananas",
        "Mango",
        "Avokado",
        "Hurmo",
        "Sabzi",
        "Kartoshka",
        "Piyoz",
        "Sarimsoq",
        "Qovoq",
        "Baqlajon",
        "Qalampir",
        "Bodring",
        "Pamidor",
        "Ko‘kat",
        "Ismaloq",
        "Sholg‘om",
        "Lavlagi",
        "Turp",
        "Karam",
        "Gulkaram",
        "Brokkoli",
        "Qizilcha",
        "Ziravorlar",
        "Grechka",
        "Guruch",
        "Makkajo‘xori",
        "Loviya",
        "No‘xat",
        "Yashil no‘xat",
        "Dukkaklilar",
        "Yong‘oq",
        "Bodom",
        "Pista",
        "Kaju",
        "Findiq",
    ]
    for product in products:
        cursor.execute(
            "INSERT OR IGNORE INTO products (product_name) VALUES (?)", (product,)
        )

    # Qutilar jadvali
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS boxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            packaging_company TEXT NOT NULL,
            export_company TEXT NOT NULL,
            box_type_id INTEGER,
            width INTEGER,
            height INTEGER,
            product_id INTEGER,
            box_count INTEGER,
            FOREIGN KEY (box_type_id) REFERENCES box_types(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """
    )

    # DataMatrix kodlari jadvali
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS datamatrix_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_id INTEGER,
            unique_id TEXT NOT NULL,
            FOREIGN KEY (box_id) REFERENCES boxes(id)
        )
    """
    )

    conn.commit()
    conn.close()
