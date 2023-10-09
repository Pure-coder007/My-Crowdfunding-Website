from flask import Flask, render_template, session, request, redirect, url_for, flash
from models import add_user, get_user, add_category, get_all_requests, User, get_user_by_id, is_user_admin, donated_people,set_request_status, get_donated_persons, get_user_requests, get_all_donations, add_donator, get_all_requests, add_request, add_donation, get_request_by_id, update_request_approval, conn, query_cat_id, fetch_cat
from utilities import send_otp
import mysql.connector
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
import random
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from db_setup import setup_database, config
from datetime import datetime
from werkzeug.urls import unquote

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

# OTP function
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
        minimum_amount = request.form.get('minimum_amount')

        # Assuming you can obtain the user's email from current_user
        user_email = current_user.email  # Update this line

        # Validate the form data (e.g., check for required fields)

        # Add request and category to the database
        add_request(user_email, category_name, fundraising_for, expiry_date, amount, description)

        add_category(user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount)

        flash('Request Submitted, waiting for admin approval', 'success')
        return redirect(url_for('category'))  # Redirect to the same page after submission

    return render_template('category.html')


 



# View_Requests routes (users)
@app.route('/view_request')
def view_request():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    # Get the current user's ID (assuming you have a User model with an 'id' attribute)
    user_id = current_user.id

    # Call the function to get user requests
    user_requests = get_user_requests(user_id)
    print(user_requests, 'userreq')
    for t in user_requests:
        print(t[0], 'desc')
    return render_template('view_request.html', user_requests=user_requests)



# Login route
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))









@app.route('/admin')
def admin():
    email = current_user.email
    if not is_user_admin(email):
        flash('You are not authorized to access this page!', 'danger')
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/see_donators')
def see_donators():
    data = get_donated_persons()
    return render_template('see_donators.html', data=data)




# See user requests (admin)
@app.route('/see_requests', methods=['GET', 'POST'])
def see_requests():
    # Get all user requests from the database
    requests = get_all_requests()
    

    print("User ID:", current_user.id)
    print('Request:', requests)
    
    return render_template('see_requests.html', requests=requests)


def approved_mail(email):
    msg = Message(' Congratulations your request has been approved, you can now receive donations', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Congratulations your request has been approved, you can now receive donations 🎉🎉🎉🎉🥳🥳🎆🎆🥂🥂🎇🎇'
    print('message :', msg)
    mail.send(msg)


@app.route('/approve_request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    # Retrieve the request and user_email from the database using request_id
    request, user_email = get_request_by_id(request_id)
    
    # Check if the request exists
    if request:
        # Check if the request is already approved (assuming 'approved' is a key in the dictionary)
        if not request.get('approved', False):
            # Update the request's approval status to True
            if update_request_approval(request_id, True):
                flash('Request approved successfully', 'success')
                approved_mail(user_email)  # Send email notification with user_email
                
            else:
                flash('An error occurred while approving the request', 'error')
        else:
            flash('Request is already approved', 'warning')
    else:
        flash('Request not found', 'error')
    
    return redirect(url_for('see_requests'))









# Mail function to donators
def send_mail(email):
    msg = Message('Verification Email', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'You just successfully registered on speedyhelp as a donator. Thank you 🎉🎉🎉🎉🥳🥳🎆🎆🥂🥂🎇🎇'
    print('message :', )
    mail.send(msg)



# Register donators
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if not current_user:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        first_time_donating = 1 if request.form.get('first_time_donating') == 'yes' else 0  
        gender = request.form['gender']

        
        
        # otp = random.randint(1000, 9999)
        # session['otp'] = otp
        send_mail(email)
        # Change to true if creating an admin
        add_donator(name, email, first_time_donating, gender)
        # send_otp(email)
        # flash('You are Welcome', 'success')
        return redirect(url_for('start_donating', email=email))
    return render_template('donate.html')



def approved_mail_donators(email):
    msg = Message('Thank you for your donations ❤❤❤', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Thank you for your donations on speedyhelp ❤❤❤'
    print('message :', msg)
    mail.send(msg)

@app.route('/start_donating', defaults={'id': None}, methods=['GET', 'POST'])
@app.route('/start_donating/<int:id>', methods=['GET', 'POST'])
def start_donating(id):
    all_requests = get_all_requests()
    percentage_ = {}
    balances = {}
    print(all_requests)
    for req in all_requests:
        d = query_cat_id(req['id'])  
        all_amount = sum(item[1] for item in d)
        balance = req['amount'] - all_amount
        balances[req['category_name']] = balance
        percentage = (float(all_amount)  / float(req['amount'])) * 100
        percentage_[req['category_name']] = percentage


    print(percentage_, 'hhhhhhhhhhhhhhhhhhhhhhhhhhh')

    if request.method == 'POST':
        donated_amount = float(request.form.get('amount_donated')) 
        category_name = request.form.get('selected_category')
        
        if balances[category_name] == 0:
            flash('Sorry, the donation target for this category has already been met.', 'info')
            return redirect(url_for('start_donating'))

        if donated_amount > balances[category_name]:
            flash('The donated amount exceeds the balance!', 'error')
            return redirect(url_for('start_donating'))
    return render_template('start_donating.html',  requests=all_requests, percentage=percentage_, balances=balances)





def received(email):
    msg = Message('You have just received an anonymous donation', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'You have just received an anonymous donation on speedyhelp'
    print('message :', msg)
    mail.send(msg)

def received_admin(username):
    msg = Message(f'{username} received an anonymous donation', sender='Anonymous@gmail.com', recipients=['admin@gmail.com'])
    msg.body = f'You have just received an anonymous donation on speedyhelp'
    print('message :', msg)
    mail.send(msg)


@app.route('/accept_donation/<email>/<cat_id>', methods=['GET', 'POST'])
def accept_donation(email, cat_id):
    amount_donated = request.form.get('amount_donated')
    # if amount_donated is not None:
    #     amount = float(amount_donated)
    # else:
    #     flash('Invalid amount donated', 'error')
    #     return redirect(url_for('start_donating'))
    # amount_donated = float(request.form['amount_donated'])
    donator_name = request.form["donator_name"]
    donator_email = request.form["email"]
    required_amount = float(request.form['required_amount'])
    # Add the donation and perform other actions
    add_donation(amount_donated, donator_name, required_amount, email, cat_id) 
    # donated_persons(donator_name, email, amount_donated)
    donated_people(donator_name, email, amount_donated)
    # flash('Thank you for your donations', 'success')
    approved_mail_donators(donator_email)
    print('Donated')
    received(email)
    user = get_user(email)
    received_admin(user.first_name)
    return redirect(url_for('start_donating'))












if __name__ == "__main__":
    app.run(debug=True)