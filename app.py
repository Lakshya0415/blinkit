from flask import Flask, request, redirect, url_for, session,flash, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blinkit_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()



# Default Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Don't redirect if user is just viewing the login page
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'email_not_found',
                'message': 'No account found with this email'
            }), 401
            
        if user.password != password:  # Note: In production, use proper password hashing
            return jsonify({
                'success': False,
                'error': 'invalid_password',
                'message': 'Incorrect password'
            }), 401
            
        # Login successful
        session['user_id'] = user.id
        session['user_name'] = user.name
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'message': 'Successfully logged in!'
        })

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Basic validation
        if not name or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('login'))
            
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return redirect(url_for('login'))
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists', 'error')
            return redirect(url_for('login'))
            
        try:
            new_user = User(name=name, email=email, password=password)  # Note: In production, hash the password
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('login'))
            
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))



# Category Pages
@app.route('/grocery')
def grocery():
    return render_template('grocery.html')

@app.route('/vegetable-fruits')
def vegetable_fruits():
    return render_template('vegetable_fruits.html')

@app.route('/cold-drinks')
def colddrink():
    return render_template('colddrink.html')

@app.route('/personal-care')
def personal_care():
    return render_template('personalCare.html')

@app.route('/category')
def category():
    return render_template('category.html')


# Shopping Cart Page
@app.route('/addCategory')
def addCategory():
    return render_template('addCategory.html')

# Address Page
@app.route('/address')
def address():
    return render_template('address.html')

# Payment Page
@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/map')
def map():
    return render_template('map.html')







if __name__ == '__main__':
    app.run(debug=True)
