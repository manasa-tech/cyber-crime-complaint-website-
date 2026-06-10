from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cybercrime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# User Table
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# =========================
# Complaint Table
# =========================
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    complaint_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')

import os

@app.route('/test')
def test():
    return str(os.listdir('templates'))
# =========================
# Home Page
# =========================
@app.route('/')
def home():
    return render_template('index.html')

# =========================
# Register
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# =========================
# Login
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return redirect('/dashboard')

        return "Invalid Login"

    return render_template('login.html')

# =========================
# Dashboard
# =========================
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# =========================
# File Complaint
# =========================
@app.route('/file-complaints', methods=['GET', 'POST'])
def file_complaints():

    if request.method == 'POST':

        fullname = request.form.get('fullname')
        complaint_type = request.form.get('complaint_type')
        description = request.form.get('description')

        complaint = Complaint(
            fullname=fullname,
            complaint_type=complaint_type,
            description=description
        )

        db.session.add(complaint)
        db.session.commit()

        return redirect('/my-complaints')

    return render_template('file-complaints.html')

# =========================
# My Complaints
# =========================
@app.route('/my-complaints')
def my_complaints():

    complaints = Complaint.query.all()

    return render_template(
        'my-complaints.html',
        complaints=complaints
    )

# =========================
# Track Complaints
# =========================
@app.route('/track-complaints')
def track_complaints():

    complaints = Complaint.query.all()

    return render_template(
        'track-complaints.html',
        complaints=complaints
    )

# =========================
# Profile
# =========================
@app.route('/profile')
def profile():
    return render_template('profile.html')

# =========================
# Contact
# =========================
@app.route('/contact')
def contact():
    return render_template('contact.html')

# =========================
# About
# =========================
@app.route('/about')
def about():
    return render_template('about.html')

# =========================
# Logout
# =========================
@app.route('/logout')
def logout():
    return render_template('logout.html')

# =========================
# Create Tables
# =========================
with app.app_context():
    db.create_all()

# =========================
# Run App
# =========================
if __name__ == '__main__':
    app.run(debug=True)