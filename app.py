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
            return redirect(url_for('homepage'))
    except KeyError:
        return redirect(url_for('login'))
    

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_user = user_collection.find_one({'uname' : request.form['username']})
        #print(login_user)
        if login_user:
            
            if hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username']=login_user['uname']
                return redirect(url_for('homepage'))

        return render_template('login.html',err='Invalid username/password combination')
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        existing_user = user_collection.find_one({'uname' : request.form['username']})

        if existing_user is None:
            hashpass = hashpw(request.form['pass'].encode('utf-8'), gensalt())
            user_collection.insert({'uname' : request.form['username'], 'password' : hashpass})
            return redirect(url_for('index'))
        
        return render_template('register.html',err='That username already exists!') 
    return render_template('register.html')



@app.route('/home')
def homepage():
    return render_template('index.html',data={'uname':session['username']})

@app.route('/account')
def account():
    return 'your account settings'



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