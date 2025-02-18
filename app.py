from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os, sqlite3, mysql.connector
from functools import wraps
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user
import db 

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'images'
conn = sqlite3.connect('POLIO_DB')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Khan@123",
    database="POLIO_DB"
)



login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def login_required_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'uname' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_view


# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():

    login_status = True  # Example login status
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/index.html', childget=child_data, user=user_data)
    return render_template('/users/index.html', login_status=login_status )

@app.route('/vac_schedule')
def vac_schedule():
    # Your code here
    return render_template('admin/vac_schedule.html')
@app.route('/reports')
def reports():
    # Your code for handling the reports page goes here
    return render_template('admin/reports.html')

@app.route('/users')
def users():
    # Your code for handling the users page goes here
    return render_template('admin/users.html')
@app.route('/terms')
def terms():
    # Your code for handling the terms page goes here
    return render_template('users/terms.html')


@app.route('/vac_stock')
def vac_stock():
    # Your code here
    return render_template('admin/vac_stock.html')


@app.route('/admin/adminhome')
def adminhome():
    if not session.get('logged_in'):
        return redirect("/adminlogin")
    return render_template('admin/adminhome.html')

# Admin Login
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == "POST":
        aname = request.form.get("aname")
        apswd = request.form.get("aPass")

        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s AND PASSWORD = %s"
        values = (aname, apswd)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            error_msg = "Invalid username or password"
            return render_template("admin/adminlogin.html", error_msg=error_msg)

        if aname == "admin" and apswd == "admin":
            session["aname"] = aname
            session['logged_in'] = True
            return redirect("/admin/adminhome")
        else:
            error_msg = "Invalid username or password"
            return render_template("admin/adminlogin.html", error_msg=error_msg)

    return render_template("admin/adminlogin.html")

@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('users_index'))

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pswd = request.form['Pass']

        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s AND PASSWORD = %s"
        values = (uname, pswd)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            session['uname'] = user[1]  # Store the username in the session
            login_user(User(user[0]))
            session['logged_in'] = True
            session["uname"] = uname
            return '''
                <script>
                    alert(" Login Successful");
                    window.location.href = "/";
                </script>
            '''
        else:
            return '''
                <script>
                    alert("Invalid UserName or Password");
                    window.location.href = "/login";
                </script>
            '''
    return render_template('/users/login.html')

@app.route('/users/index')
def users_index():
    # Handle the logic for the /users/index route
    return render_template('users/index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users_index'))

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        email = request.form['email']
        phno = request.form['phno']
        pswd = request.form['Pass']
        cpass = request.form['cpass']

        # Check if the username already exists in the database
        cursor = db.cursor()
        check_query = "SELECT * FROM register WHERE User_Name = %s"
        cursor.execute(check_query, (uname,))
        existing_user = cursor.fetchone()

        if existing_user:
            return '''
            <script>
                alert("Username already taken. Please choose a different username.");
                window.location.href = "/register";
            </script>
            '''
        if pswd == cpass:
            sql = "INSERT INTO register (User_Name, mail, Ph_Number, PASSWORD) VALUES (%s, %s, %s, %s)"
            values = (uname, email, phno, pswd)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("REGISTRATION SUCCESSFUL");
                window.location.href = "/login";
            </script>
            '''
        else:
            return '''
            <script>
                alert("PLEASE ENTER CORRECT PASSWORD");
                window.location.href = " /register";
            </script>
            '''
    return render_template('/users/register.html')


# Forgotten Password
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        uname = request.form['uname']
        npass = request.form['npass']
        cpass = request.form['cpass']

        if npass == cpass:
            cursor = db.cursor()
            cursor = db.cursor()
            sql = "UPDATE register SET PASSWORD = %s WHERE USER_NAME = %s"
            values = (npass, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("RESET PASSWORD SUCCESSFUL");
                window.location.href = "/login";
            </script>
            '''
        else:
            return '''
            <script>
                alert("PLEASE ENTER CORRECT PASSWORD")
                window.location.href = "/forgot"
            </script>
            '''
    return render_template('/users/forgot.html')

# Book Vaccine and Update Profile
@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            # Check if the form is for booking vaccine or updating profile
            if 'uname' in session and 'email' in request.form:
                uname = session['uname']
                # Update Profile
                updated_username = request.form.get('uname')
                updated_email = request.form.get('email')
                updated_phone_number = request.form.get('phno')
                updated_password = request.form.get('Pass')

                # Update the user details in the database
                cursor = db.cursor()
                sql = "UPDATE register SET USER_NAME = %s, MAIL = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
                values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
                cursor.execute(sql, values)
                db.commit()
                return '''
                <script>
                    alert("Profile Updated Successfully");
                    window.location.href = "/";
                </script>
                '''
            elif 'mname' in request.form:
                # Book Vaccine
                mname = request.form['mname']
                fname = request.form['fname']
                cname = request.form['cname']
                dob = request.form['dob']
                gender = request.form['gender']
                idproof = request.form['idproof']
                idno = request.form['idno']
                state = request.form['state']
                dist = request.form['dist']
                town = request.form['town']
                center = request.form['center']
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Perform database insertion
                cursor = db.cursor()
                sql = "INSERT INTO polio_db.book (Mother_Name, Father_Name, Child_name, Child_DOB, Gender, ID_Proof, ID_No, State, District, Town, Center) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (mname, fname, cname, dob, gender, idproof, idno, state, dist, town, center)
                cursor.execute(sql, values)
                db.commit()
                print(values)
                return '''
                <script>
                    alert("Vaccine Booking Successful");
                    window.location.href = "/";
                </script>
                '''

        uname = session['uname']
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/book.html', childget=child_data, user=user_data)

    return render_template('/users/book.html')


@app.route('/vac_detail', methods=['GET', 'POST'])
def vac_detail():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/vac_detail.html', childget=child_data, user=user_data)
    return render_template('/users/vac_detail.html')
# Vaccine Drive
@app.route('/vac_drive', methods=['GET', 'POST'])
def vac_drive():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/vac_drive.html', childget=child_data, user=user_data)
    return render_template('/users/vac_drive.html')


# Child Details
@app.route('/child_detail', methods=['GET', 'POST'])
def child_detail():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/child_detail.html', childget=child_data, user=user_data)

    # Handle the case when user data is not found or user is not logged in
    return render_template('/users/child_detail.html')

@app.route('/childsubmit', methods=['POST', 'GET'])
def childsubmit():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            user_name = session['uname']
            child_name = request.form['child_name']
            mother_name = request.form['mother_name']
            father_name = request.form['father_name']
            date_of_birth = request.form['date_of_birth']
            blood_group = request.form['blood_group']
            doses_taken = int(request.form['doses_taken'])  # Convert to int
            max_doses = 4
            doses_left = max_doses - doses_taken  # Calculate doses_left based on doses_taken
            gender = request.form['gender']
            address = request.form['address']

            # Create a cursor to execute SQL queries
            cursor = db.cursor()

            # Prepare the SQL query
            sql = "INSERT INTO child (User_name, child_name, mother_name, father_name, date_of_birth, blood_group, doses_taken, doses_left, gender, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (user_name, child_name, mother_name, father_name, date_of_birth, blood_group, doses_taken, doses_left, gender, address)
            cursor.execute(sql, values)

            # Commit the changes to the database
            db.commit()

            # Close the cursor
            cursor.close()

            return '''
            <script>
                alert("Data Stored Successfully");
                window.location.href = "/";
            </script>
            '''

    # Handle the case when user data is not found or user is not logged in
    return render_template('/users/childsubmit.html')

# Child Get
@app.route('/childget', methods=['POST', 'GET'])
def childget():
    if 'uname' in session:
        uname = session['uname']
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM child WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        if child_data:
            return render_template('/users/childget.html', childget=child_data)

    # Handle the case when user data is not found or user is not logged in
    return render_template('/users/childget.html')


# Other Vaccine
@app.route('/other_vaccine', methods=['POST', 'GET'])
def other_vaccine():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/other_vaccine.html', childget=child_data, user=user_data)
    return render_template('/users/other_vaccine.html')


# About Page
@app.route('/about', methods=['POST', 'GET'])
def about():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/about.html', childget=child_data, user=user_data)
    return render_template('/users/about.html')

# Dose 1
@app.route('/dose1', methods=['POST', 'GET'])
def dose1():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/dose1.html', childget=child_data, user=user_data)
    return render_template('/users/dose1.html')



# Dose 2
@app.route('/dose2', methods=['POST', 'GET'])
def dose2():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/dose2.html', childget=child_data, user=user_data)
    return render_template('/users/dose2.html')


# Dose 3
@app.route('/dose3', methods=['POST', 'GET'])
def dose3():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/dose3.html', childget=child_data, user=user_data)
    return render_template('/users/dose3.html')


# Dose 4
@app.route('/dose4', methods=['POST', 'GET'])
def dose4():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
    # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/dose4.html', childget=child_data, user=user_data)
    return render_template('/users/dose4.html')
     
@app.route('/vac1', methods=['POST','GET'])
def vac1():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
        # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/vac1.html', childget=child_data, user=user_data)
    return render_template('/users/vac1.html')

# Vaccine 
@app.route('/vac2', methods=['POST', 'GET'])
def vac2():
    if 'uname' in session:
        uname = session['uname']
        if request.method == 'POST':
            # Get the updated values from the form
            updated_username = request.form.get('uname')
            updated_email = request.form.get('email')
            updated_phone_number = request.form.get('phno')
            updated_password = request.form.get('Pass')

            # Update the user details in the database
            cursor = db.cursor()
            sql = "UPDATE register SET USER_NAME = %s, mail = %s, Ph_Number = %s, PASSWORD = %s WHERE USER_NAME = %s"
            values = (updated_username, updated_email, updated_phone_number, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''
        # Retrieve user data from the childget table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        values = (uname,)
        cursor.execute(sql, values)
        child_data = cursor.fetchall()

        # Retrieve user data from the register table
        cursor = db.cursor()
        sql = "SELECT * FROM register WHERE USER_NAME = %s"
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if child_data:
            return render_template('/users/vac2.html', childget=child_data, user=user_data)
    return render_template('/users/vac2.html')

# Serve Static Files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# User Info
@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    uname = session.get('uname')
    
    # Retrieve user data from the database
    cursor = db.cursor()
    sql = "SELECT * FROM register WHERE USER_NAME = %s"
    values = (uname,)
    cursor.execute(sql, values)
    user_data = cursor.fetchone()
    
    if user_data:
        user = {
            'id': user_data[0],
            'username': user_data[1],
            'email': user_data[2],
            'phone_number': user_data[3],
            'password': user_data[4]
        }
        return render_template('/users/index.html', user_data=user)
    else:
        return "User not found"



# Admin View
@app.route('/admin')
@login_required_admin
def admin_view():
    registered_users = User.query.all()
    # booked_vaccines = Vaccine.query.all()
    # return render_template('/admin/admin_view.html', registered_users=registered_users, booked_vaccines=booked_vaccines)

# Booked Vaccine
@app.route('/booked_vaccines', methods=['GET'])
def booked_vaccines():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT * FROM book"
        cursor.execute(sql)
        user_details = cursor.fetchall()
        # Don't close the connection here since you'll use it to fetch data.       
        return render_template('/admin/booked_vaccines.html', user_details=user_details)


# Registered Users
import datetime
@app.route('/registered_users', methods=['GET'])
def registered_users():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT * FROM register"
        cursor.execute(sql)
        user_details = cursor.fetchall()
        # Don't close the connection here since you'll use it to fetch data.
        current_date = datetime.datetime.now()
        
        return render_template('/admin/registered_users.html', user_details=user_details, current_date=current_date)

app.config['DEBUG'] = True

if __name__ == "__main__":
    app.run(debug=True)
