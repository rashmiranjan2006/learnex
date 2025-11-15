
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from backend.db import get_db, close_db, init_db
import os
from backend.profile import bp as profile_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random value
app.teardown_appcontext(close_db)

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/live-classes')
def live_classes():
    return render_template('live-classes.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM students WHERE email = ?', (email,)).fetchone()
        print(f"Login attempt for email: {email}")
        print(f"User record from DB: {dict(user) if user else None}")
        if user:
            password_check = check_password_hash(user['password'], password)
            print(f"Password check: {password_check}")
        else:
            print("No user found with that email.")
        if user and check_password_hash(user['password'], password):
            session['student_id'] = user['id']
            session['student_name'] = user['name']
            session['student_email'] = user['email']
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        try:
            db.execute(
                'INSERT INTO students (name, email, password) VALUES (?, ?, ?)',
                (name, email, generate_password_hash(password))
            )
            db.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'danger')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/student-dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute('SELECT * FROM students WHERE id = ?', (session['student_id'],)).fetchone()
    return render_template('student-dashboard.html', user=user)

@app.route('/stories')
def stories():
    return render_template('stories.html')

@app.route('/teachers')
def teachers():
    return render_template('teachers.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/yes')
def yes():
    return render_template('yes.html')

# Use before_request to ensure DB is initialized (compatible with all Flask versions)
@app.before_request
def initialize_database():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

app.register_blueprint(profile_bp)
if __name__ == '__main__':
    app.run(debug=True)
