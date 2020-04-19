from flask import Flask,request,session,render_template,url_for,redirect
from flask_pymongo import PyMongo
from bcrypt import hashpw,gensalt
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"]="mongodb://localhost:27017/Eventime"
app.secret_key = 'mysecret'

mongo = PyMongo(app)
user_collection=mongo.db.users
event_collection=mongo.db.events
dept_collection=mongo.db.departments
current_user=None
DATE_FORMAT='%d/%m/%y %I:%M %p'
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



@app.route('/home', methods=['GET','POST'])
def homepage():
    global current_user
    current_user=user_collection.find_one({'uname' : session['username']})
    events=event_collection.find({},{'_id':1,'name':1,'description':1})
    return render_template('index.html',current_user=current_user,data={'events':events})

@app.route('/account')
def account():
    return 'your account settings'

@app.route('/event/<query>')
def event(query):
    tevent=event_collection.find_one({'_id': ObjectId(query)})
    print(tevent)
    return render_template('event.html',current_user=current_user,tevent=tevent)

@app.route('/event/new',methods=['GET','POST'])
def addEvent():
    if request.method=='POST':
        timing=request.form['datetimes']
        stTime,endTime=timing.split('-')
        stTime=datetime.strptime(stTime.rstrip(),DATE_FORMAT)
        endTime=datetime.strptime(endTime.lstrip(),DATE_FORMAT)
        newEvent={
        'name':request.form['ename'],
        'description':request.form['descp'],
        'start':stTime,
        'end':endTime,
        'dept_name':request.form['dept'],
        'venue':request.form['venue']}
        eventId=event_collection.insert_one(newEvent).inserted_id
        return redirect(url_for('.event',query=str(eventId)))
    else:
        dept_list=dept_collection.find()
        
        return render_template('add_event.html',current_user=current_user,data={'dept':dept_list})


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