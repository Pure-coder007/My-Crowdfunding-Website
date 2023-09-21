from flask import Flask, render_template, session, request, redirect, url_for, flash
from models import add_user
import mysql.connector


app = Flask(__name__)
app.secret_key = 'language007'

@app.route('/register')
def index():
    return render_template('register.html')
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        confirm_email = request.form['confirm_email']
        password = request.form['password']
        
        if email == confirm_email:
            add_user(first_name, last_name, email, password)
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Emails do not match!', 'danger')
            return redirect(url_for('index'))
        
        
        
        
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if email == 'user@gmail.com' and password == 'password':
        flash('Login successful', 'success')
    
    
    
    
    
    
        
if __name__ == "__main__":
        app.run(debug=True)