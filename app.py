from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cybercrime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# USER TABLE
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

# COMPLAINT TABLE
class Complaint(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    complaint_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(500),
        nullable=False
    )

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# LOGIN PAGE
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
            return redirect('/complaint')

        return "Invalid Email or Password"

    return render_template('login.html')

# COMPLAINT PAGE
@app.route('/complaint', methods=['GET', 'POST'])
def complaint():

    if request.method == 'POST':

        fullname = request.form['fullname']
        complaint_type = request.form['complaint_type']
        description = request.form['description']

        new_complaint = Complaint(
            fullname=fullname,
            complaint_type=complaint_type,
            description=description
        )

        db.session.add(new_complaint)
        db.session.commit()

        return "Complaint Submitted Successfully"

    return render_template('complaint.html')

# RUN SERVER
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)