from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from backend.db import get_db
import os

bp = Blueprint('profile', __name__, url_prefix='/profile')

UPLOAD_FOLDER = 'static/images/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['POST'])
def update_profile():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute('SELECT * FROM students WHERE id = ?', (session['student_id'],)).fetchone()
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')
    photo = user['photo'] if 'photo' in user.keys() else None
    # Handle photo upload
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{user['id']}_" + file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            # Always store the path relative to /static/
            if filepath.startswith('static/'):
                photo = '/' + filepath.replace('static/', 'static/', 1)
            else:
                photo = '/static/images/profiles/' + filename
    db.execute('UPDATE students SET name=?, email=?, phone=?, photo=? WHERE id=?', (name, email, phone, photo, user['id']))
    db.commit()
    session['student_name'] = name
    session['student_email'] = email
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('student_dashboard'))
