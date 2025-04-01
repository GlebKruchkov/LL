from db_connector import DBConnection
from datetime import datetime

conn = DBConnection()


def cleanup_database():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        table_exists = cur.fetchone()[0]

        if table_exists:
            cur.execute("DELETE FROM users;")
            conn.commit()



def is_nickname_unique(nickname):
    with conn.cursor() as cur:
        query = "SELECT id FROM users WHERE nickname = %s;"
        cur.execute(query, (nickname,))
        return cur.fetchone() is None


def is_login_unique(login):
    with conn.cursor() as cur:
        query = "SELECT id FROM users WHERE login = %s;"
        cur.execute(query, (login,))
        return cur.fetchone() is None


def is_email_unique(email):
    with conn.cursor() as cur:
        query = "SELECT id FROM users WHERE email = %s;"
        cur.execute(query, (email,))
        return cur.fetchone() is None



def create_table_users():
    with conn.cursor() as cur:
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                nickname TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                phone_number TEXT NOT NULL,
                auth_token TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        cur.execute(query)
        conn.commit()


def insert_into_users(login, password, email, nickname, date_of_birth, phone_number):
    with conn.cursor() as cur:
        query = """
            INSERT INTO users (login, password, email, nickname, date_of_birth, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(query, (login, password, email, nickname, date_of_birth, phone_number))
        inserted_id = cur.fetchone()[0]
        conn.commit()
        return inserted_id


def get_user_by_login(login):
    with conn.cursor() as cur:
        query = "SELECT * FROM users WHERE login = %s;"
        cur.execute(query, (login,))
        user = cur.fetchone()
        return user


def get_user_by_nickname(nickname):
    with conn.cursor() as cur:
        query = "SELECT * FROM users WHERE nickname = %s;"
        cur.execute(query, (nickname,))
        user = cur.fetchone()
        return user


def update_user_auth_token(user_id, auth_token):
    with conn.cursor() as cur:
        query = """
            UPDATE users
            SET auth_token = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cur.execute(query, (auth_token, user_id))
        conn.commit()


def update_user_profile(current_nickname, new_nickname, date_of_birth, phone_number):
    with conn.cursor() as cur:
        query = """
            UPDATE users
            SET nickname = %s, date_of_birth = %s, phone_number = %s, updated_at = %s
            WHERE nickname = %s;
        """
        cur.execute(query, (new_nickname, date_of_birth, phone_number, datetime.now(), current_nickname))
        conn.commit()


def close_connection():
    conn.close()
