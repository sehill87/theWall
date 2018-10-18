from flask import Flask, render_template, request, redirect, session, flash, url_for
import re 
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'secrets'
mysql = connectToMySQL('simpleWall')
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

def validateRegistration():
    if len(request.form['first_name']) < 1:
        flash('First name cannot be blank', 'first_name')
    elif any(char.isalpha() for char in request.form['first_name']) == False:
        flash('First name cannot contain numbers or characters', 'first_name')
    else:
        session['first_name'] = request.form['first_name']

    if len(request.form['last_name']) < 1:
        flash('Last name cannot be blank', 'last_name')
    elif any(char.isalpha() for char in request.form['last_name']) == False:
        flash('Last name cannot contain numbers or characters', 'last_name')
    else:
         session['last_name'] = request.form['last_name']  

    mysql = connectToMySQL('simpleWall')
    email = request.form['email']
    if not email:
        flash("Email cannot be blank.", 'email')
    elif not EMAIL_REGEX.match(email):
        flash("Not a valid email", 'email')
    else: 
        session['email'] = request.form['email']
    emails = mysql.query_db("select email from users;")
    print(emails)
    print(email)
    for x in emails:
        if email == x['email']:
            flash("Email already exists", 'email')
    
   
    if len(request.form['password']) < 1:
        flash('Password cannot be blank', 'password')
    elif len(request.form['password']) < 8:
        flash('Password must be at least 8 characters', 'password')
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contian at least one upper and lowercase letter and one digit', 'password')
    else:
        session['password'] = request.form['password']
    #validate confirm password goes here
    if len(request.form['c_password']) < 1:
        flash('Confirm password cannot be blank', 'c_password')
    elif request.form['c_password'] != request.form['password']:
        flash('Passwords do not match', 'c_password')
    else:
        session['c_password'] = request.form['c_password']
    
    if '_flashes' in session.keys():
        return False
    else:
        return True
  
    #validate login
def validate_login():
    mysql = connectToMySQL('simpleWall')
    email = request.form['email']
    query = "select email from users where email = %(email)s;"
    data = {
        'email' : email
    }
    emails = mysql.query_db(query,data)
    print(email)
    print(emails)
    
    if not email:
        flash("Email cannot be blank.", 'email1')
    elif not EMAIL_REGEX.match(email):
        flash("Not a valid email", 'email1')
    elif emails == False:
        flash("User does not exist", 'email1')
    else:
        session['email'] = request.form['email']

    if len(request.form['password']) < 1:
        flash('Password cannot be blank', 'password1')
    elif len(request.form['password']) < 8:
        flash('Password must be at least 8 characters', 'password1')
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contian at least one upper and lowercase letter and one digit', 'password1')
    else:
        session['password'] = request.form['password']

    

    if '_flashes' in session.keys():
        flash('Invalid login, please return to login page!', 'not_logged_in')
        return False
    else:
        return True

    #app.route here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if validateRegistration() == False:
        return redirect('/')
    else:
        mysql = connectToMySQL('simpleWall')
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],       
        'email': request.form['email'],
        'password' : pw_hash
        }
        print(data)
        new_user = mysql.query_db(query, data)
        session['userid'] = new_user
        return redirect('/success')

@app.route('/login_validation', methods=['POST'])
def validateLogin():
    if validate_login() == False:
        return redirect('/')
    else:
        mysql = connectToMySQL('simpleWall') 
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { "email" : request.form['email'] }
        result = mysql.query_db(query, data)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                session['userid'] = result[0]['id']
                return redirect('/logged_in')
    flash('Incorrect password', 'password')
    return redirect('/')

@app.route('/logged_in')
def loggedIn():
    if not'userid' in session.keys():
        flash('User not loggged in', 'not_logged_in')
    if "_flashes" in session.keys():
        return redirect('/')
    mysql = connectToMySQL('simpleWall')
    query = "select * from users where id = %(id)s"
    data = {
        'id' : session['userid'],
        'Y' : "%m-%d-%Y",
        'T' : "%h:%i:%s" "%p"
    }
    user = mysql.query_db(query, data)
    user = user[0]
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']
    session['email'] = user['email']  
    
    mysql = connectToMySQL('simpleWall')
    query = "SELECT users.first_name, messages.message, messages.id, DATE_FORMAT(messages.created_at, %(Y)s ' @ ' %(T)s) from users join messages on users.id = messages.sender_id where recipient_id = %(id)s ORDER BY messages.created_at DESC"
    messages = mysql.query_db(query, data)
    print(messages)
    
    # mysql = connectToMySQL('simpleWall')
    # query = "SELECT DATE_FORMAT(created_at, %(Y)s) from messages where recipient_id = %(id)s"
    # date = mysql.query_db(query, data)

    #print(date, 'this should be the year')

    mysql = connectToMySQL('simpleWall')
    query = 'SELECT count(*) from messages where recipient_id = %(id)s'
    count = mysql.query_db(query, data)
    print('this is the count', count[0]["count(*)"])

    mysql = connectToMySQL('simpleWall')
    query = 'SELECT count(*) from messages where sender_id = %(id)s'
    sender_count = mysql.query_db(query, data)

    mysql = connectToMySQL('simpleWall')
    query = 'SELECT * from users where id != %(id)s'
    user_list = mysql.query_db(query, data)
    print(user_list)
    return render_template('login_page.html', user_names = user_list, messages = messages, count = count[0]['count(*)'], sender_count = sender_count[0]['count(*)'])

@app.route('/sendMessages', methods=['POST'])
def messages():
    print(request.form, "this is to see whats happening. ")
    mysql = connectToMySQL('simpleWall')
    query = "INSERT INTO messages (message, sender_id, recipient_id, created_at, updated_at) VALUES (%(message)s, %(sender_id)s, %(recipient_id)s, NOW(), NOW());"
    data = {
        'message' : request.form['message'],
        'sender_id' : session['userid'],
        'recipient_id' : request.form['recipient_id']
    }
    print(data)
    print("this is the request", request.form)
    new_message_id = mysql.query_db(query, data)
    
    return redirect('/logged_in')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete/<message_id>')
def delete(message_id):
    mysql = connectToMySQL('simpleWall')
    query = "DELETE FROM messages where id = %(id)s;"
    data = {
        "id" : int(message_id)
    }
    mysql.query_db(query, data)
    return redirect('/logged_in')

def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)