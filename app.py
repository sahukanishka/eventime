from flask import Flask,request,session,render_template,url_for,redirect
from flask_pymongo import PyMongo
from bcrypt import hashpw,gensalt

app = Flask(__name__)

app.config["MONGO_URI"]="mongodb://localhost:27017/Eventime"
app.secret_key = 'mysecret'

mongo = PyMongo(app)
user_collection=mongo.db.users



@app.route('/')
def index():
    try:
        if session['username']:
            return 'You are logged in as ' + session['username']
    except KeyError:
        return redirect(url_for('homepage'))
    

@app.route('/login', methods=['POST'])
def login():
    
    login_user = user_collection.find_one({'uid' : request.form['username']})

    if login_user:
        if hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username']=login_user['uid']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        existing_user = user_collection.find_one({'uname' : request.form['username']})

        if existing_user is None:
            hashpass = hashpw(request.form['pass'].encode('utf-8'), gensalt())
            users.insert({'uname' : request.form['username'], 'password' : hashpass})
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/home')
def homepage():
    render_template('index.html')

@app.route('/logout')
def logout():
    try:
        if session['username']:
            session.pop('username',None)

        return redirect(url_for('index'))
    except KeyError as identifier:
        return redirect(url_for('index'))
    
    


if __name__ == '__main__':
    app.run(debug=True)