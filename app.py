from flask import Flask, jsonify, request, render_template
import re
import bcrypt
import mysql.connector
import time

app = Flask(__name__)

def check_email(email):
    return True if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) else False

def connection():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="712285345"
        )
        return con
    except Exception as e:
        return jsonify({"Error": f"{e}"})

def hashing(pwd):
    pwd = pwd.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())

def setup_database():
    con = connection()
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS loyiha")
    cur.execute("USE loyiha")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    """)
    con.commit()
    con.close()

@app.route("/", methods=['GET'])
def home():
    return render_template("./main.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template("./register.html")
        if request.method == 'POST':
            data = request.form
            username = data.get('username', None)
            email = data.get('email', None)
            password = data.get('password', None)

            if username is None or len(username.strip()) < 3:
                return jsonify({"message": "Name is not full"}), 400
            if email is None or not check_email(email):
                return jsonify({"message": "Email wrong"}), 400
            if password is None or len(password.strip()) < 4 or len(password.strip()) > 32:
                return jsonify({"message": "Password wrong"}), 400

            con = connection()
            cur = con.cursor()
            cur.execute("USE loyiha")
            
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return jsonify({"message": "Email already exists"}), 400
            
            sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            val = (username, email, hashing(password))
            cur.execute(sql, val)
            con.commit()
            con.close()


            return  render_template("./login.html")
    except Exception as e:
        return jsonify({"Error": f"{e}"}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template("./login.html")
        if request.method == 'POST':
            data = request.form
            email = data.get('email', None)
            password = data.get('password', None)

            if email is None or not check_email(email):
                return jsonify({"message": "Email wrong"}), 400
            if password is None or len(password.strip()) < 4:
                return jsonify({"message": "Password wrong"}), 400

            con = connection()
            cur = con.cursor()
            cur.execute("USE loyiha")

            cur.execute("SELECT password FROM users WHERE email = %s", (email,))
            data_sql = cur.fetchone()
            if not data_sql:
                return jsonify({"message": "Email not found"}), 404
            
            hashed_password = data_sql[0]

            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return jsonify({"message": "Incorrect password"}), 401
            return render_template("success.html")
        
    except Exception as e:
        return jsonify({"Error": f"{e}"}), 500

if __name__ == "__main__":
    setup_database()
    app.run(debug=True, host="0.0.0.0")
