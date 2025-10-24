import bcrypt
from db_connection import get_db_connection

def signup(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        print("✅ User registered successfully!")
    except Exception as e:
        print("⚠️ Error:", e)
    finally:
        cursor.close()
        conn.close()


def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    record = cursor.fetchone()

    if record:
        stored_password = record[0].encode('utf-8') if isinstance(record[0], str) else record[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print("✅ Login successful!")
        else:
            print("❌ Wrong password.")
    else:
        print("❌ Username not found.")

    cursor.close()
    conn.close()
