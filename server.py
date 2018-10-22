from flask import Flask, render_template, request, redirect, session, flash, url_for
import re 
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'secrets'
mysql = connectToMySQL('register_login')
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

# Validate registration
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
    #set variables
    mysql = connectToMySQL('register_login')
    email = request.form['email']
    query = "select email from users where email = %(email)s;"
    data = {
        'email' : email
    }
    emails = mysql.query_db(query,data)
    print(email)
    print(emails)
    
    #validate email
    if not email:
        flash("Email cannot be blank.", 'email1')
    elif not EMAIL_REGEX.match(email):
        flash("Not a valid email", 'email1')
    elif emails == False:
        flash("User does not exist", 'email1')
    else:
        session['email'] = request.form['email']

    #validate password
    if len(request.form['password']) < 1:
        flash('Password cannot be blank', 'password1')
    elif len(request.form['password']) < 8:
        flash('Password must be at least 8 characters', 'password1')
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contian at least one upper and lowercase letter and one digit', 'password1')
    else:
        session['password'] = request.form['password'] 

    if '_flashes' in session.keys():
        flash('Invalid login:', 'not_logged_in')
        return False
    else:
        return True

#validate quotes
def validate():
    if len(request.form['author']) < 1:
        flash('Author cannot be blank', 'author')
    else:
        session['author'] = request.form['author']

    if len(request.form['quote']) < 1:
        flash('Quote cannot be blank', 'quote')
    else:
        session['quote'] = request.form['quote']
    
    if '_flashes' in session.keys():
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
        mysql = connectToMySQL('register_login')
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
        mysql = connectToMySQL('register_login') 
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
    mysql = connectToMySQL('register_login')
    query = "select * from users where id = %(id)s"
    data = {
        'id' : session['userid'],
    }
    user = mysql.query_db(query, data)
    user = user[0]
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']
    session['email'] = user['email']  
    
    mysql = connectToMySQL('register_login')
    query = 'SELECT id, author, quote, user_id from quotes'
    
    quotes = mysql.query_db(query, data)
    
    print(quotes)
    print(session['userid'])
    mysql = connectToMySQL('register_login')
    query = 'SELECT count(*) from likes where wish_id = 17'
    like_count = mysql.query_db(query)
    return render_template('logged_in.html', quotes = quotes)


@app.route('/success')
def success():
    if not'userid' in session.keys():
        flash('User not loggged in', 'not_logged_in')
        return redirect('/')
    return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/user_quotes')
def user_quotes():
    if not'userid' in session.keys():
        flash('User not loggged in', 'not_logged_in')
        return redirect('/')
    mysql = connectToMySQL('register_login')
    query = "SELECT * FROM quotes WHERE user_id = %(id)s"
    data = {
        'id' : session['userid'],
        
    }
    user_quotes = mysql.query_db(query, data)

    return render_template('user_quotes.html', quotes = user_quotes)

@app.route('/validate_quotes', methods=['POST'])
def validate_quotes():
    if validate() == False:
        print(False)
        return redirect('/logged_in')
    else:
        mysql = connectToMySQL('register_login')
        query = "INSERT INTO quotes (author, quote, user_id, created_at, updated_at) VALUES (%(author)s, %(quote)s, %(user_id)s, NOW(), NOW());"
        data = {
            'author' : request.form['author'],
            'user_id' : session['userid'],
            'quote' : request.form['quote']
        }
        quotes = mysql.query_db(query, data)
    return redirect('/logged_in')


@app.route('/delete/<quote_id>')
def delete_wish(quote_id):
    mysql = connectToMySQL('register_login')
    query = "DELETE FROM quotes where id = %(id)s;"
    data = {
        "id" : int(quote_id)
    }
    mysql.query_db(query, data)
    return redirect('/logged_in')

@app.route("/edit/<user_id>/user")
def edit(user_id):
    if not'userid' in session.keys():
        flash('User not loggged in', 'not_logged_in')
        return redirect('/')
    
    data = {
        "id" : session['userid']
    }
    mysql = connectToMySQL('register_login')
    query = "Select * from users where id = %(id)s"
    edit_user = mysql.query_db(query, data)
    print(edit_user)
    id = session['userid']
    print(id)
    return render_template('edit.html', update = edit_user, id = user_id)

@app.route("/edit/<id>", methods=['POST'])
def update(id):
    data = {
        "id" : id,
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email']
    }
    mysql = connectToMySQL('register_login')
    query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, updated_at = NOW() where id = %(id)s;"
    mysql.query_db(query, data)
    return redirect('/logged_in')

@app.route('/like/<grant_id>')
def like(grant_id):
    print(grant_id)
    mysql = connectToMySQL('register_login')
    query = "INSERT INTO likes (user_id, wish_id) VALUES (%(user_id)s, %(grant_id)s)"
    data = {
        'user_id' : session['userid'],
        'grant_id' : int(grant_id)
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