from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# MongoDB connection setup
client = MongoClient("127.0.0.1:27017")  # Use your MongoDB URI
db = client['Details_db']  # Database name
users_collection = db['data']  # Collection for user data

# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Register route (for simplicity)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = sha256_crypt.hash(password)

        # Store user in MongoDB
        users_collection.insert_one({'first_name':first_name ,'last_name':last_name ,'email': email, 'password': hashed_password})

        flash("Registration Successful!", "success")
        return redirect(url_for('loginpage'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if user exists
    email= users_collection.find_one({'email': email})
    
    if email and sha256_crypt.verify(password, email['password']):
        flash("Login Successful!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid Username or Password!", "danger")
        return redirect(url_for('home'))

if __name__== '__main__':
    app.run(debug=True)