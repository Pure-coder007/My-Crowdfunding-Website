from flask import Flask, render_template, session, request, redirect, url_for, flash
from models import add_user
import mysql.connector
from flask_login import current_user
import random
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kingsleydike318@gmail.com'
app.config['MAIL_PASSWORD'] = ' byyhvorltumsxffq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = 'language007'


# Creating random One-Time-Password
# OTP = random.randint(1000, 9999)

def send_otp(email, otp):
    msg = Message('Verification Token', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Your verification token is {otp}'
    print('otp :', otp)
    mail.send(msg)


@app.route('/')
def index():
    return render_template('index.html')
    
    
    
    
# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        confirm_email = request.form['confirm_email']
        password = request.form['password']
        
        if email == confirm_email:
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            send_otp(email, otp)
            add_user(first_name, last_name, email, password)
            # send_otp(email)
            flash('Please verify your email', 'success')
            return redirect(url_for('token', email=email))
        else:
            flash('Emails do not match!', 'danger')
        return redirect(url_for('register'))
    return render_template('register.html')
        


# OTP route
@app.route('/token/<email>', methods=['GET', 'POST'])
def token(email):
    if request.method == 'POST':
        token = request.form.get('otp')
        
        
        stored_otp = session.get('otp', None)
        if token != str(stored_otp):
            print('token:', token)
            print('otp:', stored_otp)
        # if token != otp:
            flash('Invalid Token', 'danger')
            print('invalliiidddd')
            return render_template('token.html')
        flash('Registration Successful', 'success')
        return redirect(url_for('login'))        
    return render_template('token.html')
        
        
        

# Login route

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'test@example.com' and password == 'password':
            flash('Successfully logged in', 'success')
            return redirect(url_for('category'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')



# Category route
@app.route('/category')
def category():
    pass
    return render_template('category.html')




# View_Requests routes
@app.route('/view_request')
def view_request():
    pass
    return render_template('view_request.html')












































if __name__ == "__main__":
    app.run(debug=True)