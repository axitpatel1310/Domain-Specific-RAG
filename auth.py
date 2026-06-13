from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import get_connection

def create_user(username,email,password):
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(
        password
    )
    try:
        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                password_hash
            )
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()
        
def get_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_user(email,password):
    user = get_user(email)
    if not user:
        return None
    if check_password_hash(
        user["password_hash"],
        password
    ):
        return user
    return None