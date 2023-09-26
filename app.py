from flask import Flask, render_template, session, request, redirect, url_for, flash
from models import add_user, get_user, add_category, get_requests, User, get_user_by_id, is_user_admin, set_request_status
from utilities import send_otp
import mysql.connector
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
import random
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config.from_pyfile('config.py')
# Flask mail configuration

mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


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
    if not current_user:
        return redirect(url_for('index'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        confirm_email = request.form['confirm_email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        
        if email == confirm_email:
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            send_otp(email, otp)
            # Change to true if creating an admin
            add_user(first_name, last_name, email, hashed_password, False)
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
    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user(email)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            # flash('Successfully logged in', 'success')
            session['user_id'] = user.id
            if user.is_admin:
                return redirect(url_for('admin'))

            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')



# Category route
@app.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    if request.method == 'POST':
        user_id = current_user.id
        category_name = request.form.get('category-name')
        fundraising_for = request.form.get('fundraising-for')
        amount = request.form.get('amount')
        description = request.form.get('description')
        expiry_date = request.form.get('expiryDate')
        # user_email = request.form.get('user_email')
        
        add_category(user_id, category_name, fundraising_for, expiry_date, amount, description)
        print(category, fundraising_for, amount, description, expiry_date)
        flash('Request Submitted, waiting for admin approval', 'success')
        return redirect(url_for('category'))
    return render_template('category.html')





# View_Requests routes
@app.route('/view_request')
def view_request():
    if not current_user:
        return redirect(url_for('index'))
    requests = get_requests()
    return render_template('view_request.html')


# Login route
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route("/donate", methods=['GET', 'POST'])
def donate():
    return redirect(url_for('donate'))



@app.route('/admin')
def admin():
    email = current_user.email
    if not is_user_admin(email):
        flash('You are not authorized to access this page!', 'danger')
        return redirect(url_for('login'))

    return render_template('admin.html')


@app.route('/see_donators')
def see_donators():
    pass
    return render_template('see_donators.html')



@app.route('/see_requests')
def see_requests():
    
    if not current_user:
        return redirect(url_for('index'))
    my_requests = get_requests()
    print('Request:', my_requests)
    
    my_requests = get_requests()
    
    # Formatting the expiry_date for each request
    for request_ in my_requests:
        request_['expiry_date'] = request_['expiry_date'].strftime('%m/%d/%y')
    
    if not current_user.is_admin:
        flash('You are not authorized to access this page!', 'danger')
        return redirect(url_for('index'))
    return render_template('see_requests.html', my_requests=my_requests)



@app.route('/approve_request/<int:request_id>', methods=['POST'])
@login_required
def approve_request(request_id):
    if not set_request_status(request_id, "approved"):
        flash('Error approving the request. Please try again.', 'danger')
    else:
        flash('Request successfully approved.', 'success')
    return redirect(url_for('see_requests'))


@app.route('/disapprove_request/<int:request_id>', methods=['POST'])
@login_required
def disapprove_request(request_id):
    if not set_request_status(request_id, "disapproved"):
        flash('Error disapproving the request. Please try again.', 'danger')
    else:
        flash('Request successfully disapproved.', 'success')
    return redirect(url_for('see_requests'))






















if __name__ == "__main__":
    app.run(debug=True)