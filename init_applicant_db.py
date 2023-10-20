import sqlite3

DB_APPLICANT_NAME = 'applicant.db'

def init_applicant_db():
    conn = sqlite3.connect(DB_APPLICANT_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT,
            adhar TEXT NOT NULL,
            residence TEXT NOT NULL,
            permanent TEXT NOT NULL,
            pass_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_applicant_db()
    print(f"Database {DB_APPLICANT_NAME} initialized successfully.")
