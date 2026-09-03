import mysql.connector
from flask import Flask, render_template, request, redirect, session
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# MySQL Database Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT")),
    ssl_ca="ca.pem"
)

app = Flask(__name__)

# Secret key from .env
app.secret_key = os.getenv("SECRET_KEY")


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form["username"]
        mobile = request.form["mob"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE name = %s AND email = %s",
            (name, email)
        )

        search = cursor.fetchone()

        if search:
            cursor.close()
            return render_template("register.html", user_exists=True)

        else:
            cursor.execute(
                "INSERT INTO users (name, mobile, email, password) VALUES (%s, %s, %s, %s)",
                (name, mobile, email, password)
            )

            db.commit()
            cursor.close()

            return redirect('/login')

    return render_template("register.html")


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        name = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE name = %s AND password = %s",
            (name, password)
        )

        check = cursor.fetchone()

        cursor.close()

        if check:
            session["username"] = name
            return redirect('/')

        else:
            return render_template("login.html", name_exist=True)

    return render_template("login.html")


# Change Password
@app.route('/changepass', methods=['GET', 'POST'])
def change():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        newpass = request.form['newpass']

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )

        find = cursor.fetchone()

        if find:

            cursor.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                (newpass, email)
            )

            db.commit()
            cursor.close()

            return render_template("changepass.html", old=True)

        else:

            cursor.close()

            return render_template("changepass.html", new=True)

    return render_template("changepass.html")


# About Us
@app.route('/aboutus')
def about():
    return render_template("aboutus.html")


# Logout
@app.route("/logout")
def logout():

    session.pop('username', None)

    return redirect("/")


# Run Flask Application
if __name__ == '__main__':
    app.run(debug=True)