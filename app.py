from flask import Flask, render_template, request
import bcrypt
from db_connection import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html', page='home')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        message = "✅ User registered successfully! Please log in."
        return render_template('main.html', page='login', message=message)
    except Exception as e:
        return render_template('main.html', page='signup', message=f"⚠️ Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    record = cursor.fetchone()

    cursor.close()
    conn.close()

    if record and bcrypt.checkpw(password.encode('utf-8'), record[0].encode('utf-8') if isinstance(record[0], str) else record[0]):
        return render_template('main.html', page='welcome', username=username)
    else:
        return render_template('main.html', page='login', message="❌ Invalid username or password.")

if __name__ == '__main__':
    app.run(debug=True)
