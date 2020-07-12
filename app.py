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
            user_collection.insert({'uname' : request.form['username'], 'password' : hashpass,'access':request.form['category'],'department':request.form['dept']})
            return redirect(url_for('index'))
        print(request.form)
        return render_template('register.html',err='That username already exists!',username=request.form['username'],password=request.form['pass']) 
    return render_template('register.html')



@app.route('/home', methods=['GET','POST'])
def homepage():
    global current_user
    current_user=user_collection.find_one({'uname' : session['username']})
    events=event_collection.find({},{'_id':1,'name':1,'description':1})
    return render_template('index.html',current_user=current_user,data={'events':events})

@app.route('/account')
def account():
    uevents=event_collection.find({'_id':{'$in':current_user['events']}},{'_id':1,'name':1,'start':1})
    return render_template('user_acc.html',current_user=current_user,uevents=uevents)

@app.route('/event/<query>',methods=['GET','POST'])
def event(query):
    global current_user
    tevent=event_collection.find_one({'_id': ObjectId(query)})
    #print(rtype)
    try:
        #print("inside try")
        users=[p['pid'] for p in tevent['participants']]
        #print(users,current_user['_id'])
        participated=current_user['_id'] in users
        #print(participated)
    except:
        #print(e)
        participated=False
    if request.method=='POST':
        #update event with new partisipant
        #print(current_user['_id'])
        if rtype=='push':
            user_collection.update_one({'_id': current_user['_id']}, {'$push': {'events': ObjectId(query)}})
            event_collection.update_one({'_id': ObjectId(query)},{'$push':{'participants':{'pid':ObjectId(current_user['_id']),'name':current_user['uname'],'dept':current_user['department']}}})
        elif rtype=='pull':
            print(rtype)
            pass
        return redirect(request.url)
    print(participated)
    return render_template('event.html',current_user=current_user,tevent=tevent,participated=participated)

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

@app.route('/event/<query>/<rtype>',methods=['POST'])
def participate(query,rtype):
    global current_user
    if rtype=='push':
        user_collection.update_one({'_id': current_user['_id']}, {'$push': {'events': ObjectId(query)}})
        event_collection.update_one({'_id': ObjectId(query)},{'$push':{'participants':{'pid':ObjectId(current_user['_id']),'name':current_user['uname'],'dept':current_user['department']}}})
    elif rtype=='pull':
        event_collection.update_one({ '_id': ObjectId(query) },{ '$pull': { 'participants': { 'pid':current_user['_id']}}})
        user_collection.update_one({'_id': current_user['_id']},{'$pull': {'events': ObjectId(query)}})
    elif rtype=='update':
        event_collection.update_one({'_id': ObjectId(query)},{'$push':{'updates':{'time':datetime.now(),'desc':request.form['update-text']}}})
        print(request.form)
    elif rtype=='delupd':
        event_collection.update_one({ '_id': ObjectId(query) },{ '$unset': { 'updates.'+str(int(request.form['ind'])-1):1}})
        event_collection.update_one({'_id':ObjectId(query)},{'$pull':{'updates':None}})
        print(request.form)
    return redirect(url_for('event',query=query))

@app.route('/event/<query>/<partid>/remove',methods=['POST'])
def removePart(query,partid):
    global current_user
    user_collection.update_one({'_id': ObjectId(partid)}, {'$pull': {'events': ObjectId(query)}})
    event_collection.update_one({'_id': ObjectId(query)},{'$pull':{'participants':{'pid':ObjectId(partid)}}})
    return redirect(url_for('event',query=query))



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