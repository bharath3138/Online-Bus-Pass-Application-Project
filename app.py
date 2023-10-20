from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database configuration for registration and admin data
DB_REGISTER_NAME = 'register.db'
DB_ADMIN_NAME = 'admin.db'
DB_APPLICANT_NAME = 'applicant.db'  # Added for applicant data

# Initialize the registration database table
def init_register_db():
    conn = sqlite3.connect(DB_REGISTER_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registered_users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the admin database table
def init_admin_db():
    conn = sqlite3.connect(DB_ADMIN_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the applicant database table
def init_applicant_db():
    conn = sqlite3.connect(DB_APPLICANT_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT,
            adhar TEXT NOT NULL,
            residence TEXT NOT NULL,
            permanent TEXT NOT NULL,
            pass_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_register_db()
init_admin_db()
init_applicant_db()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # You can render a dashboard template here for authenticated users.
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))

# Route to render the application template
@app.route('/application')
def application():
    return render_template('application.html')

# Route to render the registration form
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

# Route to handle the registration form submission
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('register-email')
    password = request.form.get('register-password')
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Updated method

    conn = sqlite3.connect(DB_REGISTER_NAME)
    cursor = conn.cursor()

    # Check if the username is already taken
    cursor.execute("SELECT id FROM registered_users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return "Username already exists. Choose another username."
    else:
        cursor.execute("INSERT INTO registered_users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return "Registration successful. You can now log in."

# Add the login route, similar to your existing implementation
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('login-email')
    password = request.form.get('login-password')

    conn = sqlite3.connect(DB_REGISTER_NAME)
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT id, password FROM registered_users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        conn.close()
        return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
    else:
        conn.close()
        return "Invalid login credentials"

# Route for the admin login
@app.route('/admin-login', methods=['POST'])
def admin_login():
    admin_username = request.form.get('admin-username')
    admin_password = request.form.get('admin-password')

    conn = sqlite3.connect(DB_ADMIN_NAME)
    cursor = conn.cursor()

    # Check if the admin exists
    cursor.execute("SELECT id, password FROM admin_users WHERE username = ?", (admin_username,))
    admin = cursor.fetchone()

    if admin and check_password_hash(admin[1], admin_password):
        session['admin_id'] = admin[0]
        conn.close()
        return redirect(url_for('dashboard'))  # Redirect to dashboard on successful admin login
    else:
        conn.close()
        return "Invalid admin login credentials"

@app.route('/submit-application', methods=['POST'])
def submit_application():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        adhar = request.form.get('adhar')
        residence = request.form.get('residence')
        permanent = request.form.get('permanent')
        pass_type = request.form.get('pass-type')

        # Validate form data
        if not all([name, age, dob, gender, mobile, adhar, residence, permanent, pass_type]):
            return "Please fill in all required fields."

        conn = sqlite3.connect(DB_APPLICANT_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO applicants (name, age, dob, gender, mobile, email, adhar, residence, permanent, pass_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, dob, gender, mobile, email, adhar, residence, permanent, pass_type)
        )

        conn.commit()
        conn.close()

    return "Application submitted successfully."


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
