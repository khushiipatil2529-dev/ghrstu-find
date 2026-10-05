import sqlite3

DATABASE = "ghrstu_find.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_db_connection()

    cursor = connection.cursor()


    # ==============================
    # USERS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            college_id TEXT UNIQUE,

            role TEXT DEFAULT 'student',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # ==============================
    # ITEMS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            item_type TEXT NOT NULL,

            item_name TEXT NOT NULL,

            category TEXT,

            description TEXT,

            color TEXT,

            brand TEXT,

            identifying_marks TEXT,

            location TEXT,

            date_reported TEXT,

            image_path TEXT,

            status TEXT DEFAULT 'active',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)

        )
    """)


    # ==============================
    # CLAIMS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_id INTEGER NOT NULL,

            claimant_id INTEGER NOT NULL,

            message TEXT,

            status TEXT DEFAULT 'pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (item_id)
                REFERENCES items(id),

            FOREIGN KEY (claimant_id)
                REFERENCES users(id)

        )
    """)


    # ==============================
    # NOTIFICATIONS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            message TEXT NOT NULL,

            is_read INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)

        )
    """)


    # ==============================
    # MATCHES
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            lost_item_id INTEGER NOT NULL,

            found_item_id INTEGER NOT NULL,

            match_score REAL DEFAULT 0,

            status TEXT DEFAULT 'possible',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (lost_item_id)
                REFERENCES items(id),

            FOREIGN KEY (found_item_id)
                REFERENCES items(id)

        )
    """)


    # ==============================
    # AUDIT LOGS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            action TEXT NOT NULL,

            details TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)

        )
    """)


    connection.commit()

    connection.close()


if __name__ == "__main__":

    create_database()

    print("GHRSTU Find database created successfully!")