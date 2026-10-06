
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB = 'database.db'


# ---------- Database Connection ----------

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Create Database ----------

def init_db():

    conn = get_conn()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            profile_pic TEXT NOT NULL,

            banner TEXT NOT NULL,

            name TEXT NOT NULL,

            headline TEXT NOT NULL,

            location TEXT NOT NULL,

            skills TEXT NOT NULL,

            experience TEXT NOT NULL,

            bio TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# ---------- Home Page ----------

@app.route('/')
def users():

    conn = get_conn()

    rows = conn.execute(
        'SELECT * FROM users ORDER BY id DESC'
    ).fetchall()

    conn.close()

    return render_template(
        'users.html',
        users=rows
    )


# ---------- Add Profile Page ----------

@app.route('/add')
def add_form():

    return render_template('adduser.html')


# ---------- Save Profile ----------

@app.route('/add', methods=['POST'])
def add_user():

    profile_pic = request.form['profile_pic']

    banner = request.form['banner']

    name = request.form['name']

    headline = request.form['headline']

    location = request.form['location']

    skills = request.form['skills']

    experience = request.form['experience']

    bio = request.form['bio']


    conn = get_conn()

    conn.execute('''
        INSERT INTO users
        (
            profile_pic,
            banner,
            name,
            headline,
            location,
            skills,
            experience,
            bio
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    ''', (
        profile_pic,
        banner,
        name,
        headline,
        location,
        skills,
        experience,
        bio
    ))


    conn.commit()

    conn.close()


    return redirect(url_for('users'))


# ---------- Run Application ----------

if __name__ == '__main__':

    app.run(debug=True)
