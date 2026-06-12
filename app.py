from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# =========================
# Flask App Configuration
# =========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

# =========================
# Database Configuration
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'cybercrime.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# User Model
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# =========================
# Complaint Model
# =========================
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    complaint_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')

# =========================
# Test Route
# =========================
@app.route('/test')
def test():
    try:
        files = os.listdir(os.path.join(BASE_DIR, "templates"))
        return "<br>".join(files)
    except Exception as e:
        return str(e)

# =========================
# Home
# =========================
@app.route('/')
def home():
    return render_template('dashboard.html')

# =========================
# Register
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already exists!"

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# =========================
# Login
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return redirect(url_for('dashboard'))

        return "Invalid Email or Password"

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

        fullname = request.form['fullname']
        complaint_type = request.form['complaint_type']
        description = request.form['description']

        complaint = Complaint(
            fullname=fullname,
            complaint_type=complaint_type,
            description=description
        )

        db.session.add(complaint)
        db.session.commit()

        return redirect(url_for('my_complaints'))

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
# Create Database Tables
# =========================
with app.app_context():
    db.create_all()

# =========================
# Run App
# =========================
if __name__ == '__main__':
    print("Current Directory:", os.getcwd())
    print("Templates Folder:", os.path.join(BASE_DIR, "templates"))

    if os.path.exists(os.path.join(BASE_DIR, "templates")):
        print("Templates Found:")
        print(os.listdir(os.path.join(BASE_DIR, "templates")))
    else:
        print("Templates folder NOT FOUND!")

    app.run(debug=True)