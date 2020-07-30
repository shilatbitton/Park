from flask import Flask,render_template,request,flash,session,redirect,url_for,abort
from forms import LoginForm,SignOutForm,NewParkForm,DeleteParkForm,signupForm,signout2Form,addComment,updateComment,facilitiesForm,PostForm,infoForm
from flask_jsglue import JSGlue
import pyrebase
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
app = Flask(__name__)
jsglue = JSGlue(app)
app.config['SECRET_KEY']='mormormor'
import json 
import os
import tempfile
from werkzeug.utils import secure_filename



print(firebase_admin)
config={
  "apiKey": "AIzaSyDab7tKKm11tgRuLsAPejXGGAYJ1d20cnQ",
  "authDomain": "parkflask.firebaseapp.com",
  "databaseURL": "https://parkflask.firebaseio.com",
  "projectId": "parkflask",
  "storageBucket": "parkflask.appspot.com",
  "messagingSenderId": "685599054335",
  "appId": "1:685599054335:web:db2d1d2890588a14772fca",
  "measurementId": "G-H8HGMEE4WB"
}

with open('playgrounds.json', 'r',encoding="utf8") as myfile:
    data=json.loads(myfile.read())

cred = credentials.Certificate('parkflask-firebase-adminsdk-wplsp-87a9bb6106.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
storage=firebase.storage()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET', 'POST'])
@app.route('/homePage',methods=['GET', 'POST'])
def homePage():
        if "user" in session:
            if(session["admin"]):
                return redirect(url_for("adminPage"))
            else:
                return redirect(url_for("visitPage"))
        return render_template('homePage.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    print("login")
    form = LoginForm()
    if request.method == 'POST':
    # if form.validate_on_submit():
        print("click")
        try:
            user=auth.sign_in_with_email_and_password(form.email.data,form.password.data)
            uid=auth.get_account_info(user['idToken'])['users'][0]['localId']
            session["uid"]=uid
            doc_ref=db.collection(u"Users").document(uid)
            doc = doc_ref.get()
            if doc.exists:
                admin=doc.to_dict()['admin']
                if(admin):
                    session["admin"]=True
                    session["user"]=form.email.data
                    return redirect(url_for("adminPage"))
                else:
                    session["admin"]=False
                    session["user"]=form.email.data
                    return redirect(url_for("visitPage"))
        except:
            return render_template('index.html',form=form,us="Not Exist")
    else:
        if "user" in session:
            if(session["admin"]):
                return redirect(url_for("adminPage"))
            else:
                return redirect(url_for("visitPage"))
        print("gggggg")
        return render_template('index.html',form=form)

commentNum=0
'''
@app.route('/delete_comment',methods=['GET', 'POST'])
def delete_comment():
    form=commentForm()
    if form.validate_on_submit():
        docs=db.collection(u'Comments').stream()
        date=form.date.data
        time=form.time.data
        park=form.parkname.data
        for doc in docs:
            d=doc.to_dict()

            if date==d['date'] and time==d['time'] and park==d['parkname']:

                db.collection(u'Comments').document(doc.id).delete()
                return redirect(url_for("homePage"))

    return render_template('delete_comment.html',form=form)

'''

@app.route('/comment',methods=['GET', 'POST'])
def comment():
    global commentNum
    commentNum=commentNum+1
    form=commentForm()
    if form.validate_on_submit():
        print("hi")
        now = datetime.now()
        date=now.strftime("%d/%m/%Y")
        time=now.strftime("%H:%M:%S")
        print(date)
        print(time)
        email=form.email.data
        password=form.password.data
        parkName=form.parkname.data
        docs=db.collection(u'Users').stream()
        for doc in docs:
            d=doc.to_dict()

            if email==d['email'] and password==d['password']:
                data={'email':email,'password':password, 'comment':form.comment.data,'time':time,'date':date,'parkName':parkName}
                print(data)
                db.collection(u'Comments').document().set(data)
                print(form.comment.data)
                print(commentNum)
                print(date)
                print(time)
                return redirect(url_for("homePage"))
                break

    print(form.email.data)
    print("hiyou")
    return render_template('comment.html',form=form)





@app.route('/adminPage',methods=['GET', 'POST'])
def adminPage():
        return render_template('adminPage.html')

@app.route('/visitPage',methods=['GET', 'POST'])
def visitPage():
        return render_template('visitPage.html')



@app.route('/user',methods=['GET', 'POST'])
def user():
    if "user" in session:
        form = SignOutForm()
        if form.validate_on_submit():
            return redirect(url_for("logout"))
        return render_template('login.html',form=form)
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    print("logout")
    session.pop("user",None)
    flash("התנתקת בהצלחה")
    return redirect(url_for("homePage"))

@app.route('/register',methods=['GET', 'POST'])
def register():
    form=signupForm()
    if request.method == 'POST':
        email=form.email.data
        password=form.password.data
        name=form.name.data
        last=form.last.data
        user=auth.create_user_with_email_and_password(email,password)
        data={"name":name,"last":last,"email":email,"password":password,"admin":False}
        #db.child("Guest").push(data)
        #data2={"name":"1","other":email,"shadowing":"123"}
        #db.child("Parks").push(data2)
        print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        info=auth.get_account_info(user['idToken'])['users'][0]['localId']
        db.collection(u'Users').document(info).set(data)
        return redirect(url_for("login"))
    return render_template('basic.html',form=form)

#signup
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

#unregister
@app.route('/unregister',methods=['GET', 'POST'])
def unregister():
    form=signout2Form()
    if request.method == 'POST':
        print("in if1")
        email=form.email.data
        password=form.password.data
        docs=db.collection(u'Users').stream()
        for doc in docs:
            d=doc.to_dict()
            if email==d['email'] and password==d['password']:
                user_id=doc.id
                docs = db.collection(u'Comments').where(u'userId', u'==', user_id).stream()
                for doc in docs:
                    doc.reference.delete()
                firebase_admin.auth.delete_user(user_id)
                db.collection(u'Users').document(user_id).delete()
                session.pop("user",None)
                return redirect(url_for("homePage"))
        #user=auth.create_user_with_email_and_password(email,password)
        #data={"username":username,"email":email,"password":password}
        #db.child("Guest").push(data)
        #data2={"name":"1","other":email,"shadowing":"123"}
        #db.child("Parks").push(data2)
        #print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        #info=auth.get_account_info(user['idToken'])['users'][0]['localId']
        #db.collection(u'Guest').document(info).set(data)

    print("hello")
    return render_template('basic3.html',form=form)

@app.route('/newpark', methods =['GET','POST'])
def newpark():
    form = NewParkForm()
    if form.validate_on_submit():
        data = {
        "name": form.parkName.data,
        "other": form.parkAddress.data,
        "shadowing": form.shadow.data
        }
        docs = db.collection(u'Parks').stream()
        canMakePark = True
        for doc in docs:
            dici = doc.to_dict()
            if data["name"] == dici['name'] and data["other"] == dici['other']:
                canMakePark = False

        if canMakePark:
            db.collection(u'Parks').document().set(data)
            flash(" יצרת פארק חדש ")
        else:
            flash("לא ניתן ליצור פארק")

        return redirect(url_for('newpark'))
    return render_template('createNewPark.html', form=form,admin=session["admin"])

@app.route('/deletepark', methods =['GET','POST'])
def deletepark():
    form = DeleteParkForm()
    if form.validate_on_submit():

        req = request.form
        parkName = req["parkName"]
        parkAddress = req["parkAddress"]

        docs = db.collection(u'Parks').stream()
        for doc in docs:
            dici = doc.to_dict()
            if parkName == dici['name'] and parkAddress == dici['other']:
                print (f"park {dici['name']} in {dici['other']} has beem deleted")
                db.collection(u'Parks').document(doc.id).delete()
                flash("מחקת פארק")


        return redirect(url_for('deletepark'))
    return render_template('deletePark.html', form=form,admin=session["admin"])

@app.route('/parks',methods=['GET', 'POST'])
def parks():
        return render_template('parks.html',data=data,admin=session["admin"])

@app.route('/comments/<p>',methods=['GET', 'POST'])
def comments(p):
    form=addComment()
    rat=True
    doc = db.collection(u'Users').document(session["uid"]).get()
    c=doc.to_dict()
    try:
        if p in c['parks']:
            rat=False
    except:
        print("Not")
    docs = db.collection(u'Comments').where(u'name', u'==', p).stream()
    arr=[]
    for doc in docs:
        d=doc.to_dict()
        d["first"]=db.collection(u'Users').document(d["userId"]).get().to_dict()["name"]
        d["last"]=db.collection(u'Users').document(d["userId"]).get().to_dict()["last"]
        d["post_id"]=doc.id
        arr.append(d)
    ########## park facility
    data = {'name': p, 'userId': session["uid"], 'data-rating': form.comment.data}
    docs = db.collection(u'Parks').stream()
    for doc in docs:
        dici = doc.to_dict()
        if p == dici['name']:
            parkFacility = dici['parkFacility']
    docs = db.collection(u'Parks').where(u'name', u'==', p).stream()
    for doc in docs:
        r=doc.to_dict()
        if(r['votes']==0):
            ret=5
        else:
            ret=r['rating']/r['votes']
    
    ########## end - park facility
    if request.method == 'POST':
        data={'name':p,'userId':session["uid"],'text':form.comment.data}
        doc=db.collection(u'Comments').document()
        doc.set(data)
        f = request.files['file']
        if f.filename != '':
            filename = secure_filename(f.filename)
            print(filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            storage.child("image/"+doc.id).put("static/uploads/"+filename)
            url=storage.child("image/"+doc.id).get_url(None)
            doc.update({
                'image':url
            })
        return redirect(request.referrer)
    return render_template('comments.html',admin=session["admin"],parkName=p,email=session["user"],comments=arr,form=form,now=session["uid"],parkFacility=parkFacility,ret=ret,rat=rat)

@app.route('/comments/<post_id>/delete',methods=['GET', 'POST'])
def delete_comments(post_id):
    db.collection(u'Comments').document(post_id).delete()
    return redirect(url_for('parks'))

@app.route('/comments/<p>/<r>/rating',methods=['GET', 'POST'])
def rating(p,r):
    docs = db.collection(u'Parks').where(u'name', u'==', p).stream()
    for doc in docs:
        c=doc.to_dict()
        a=c['votes']
        b=c['rating']
    db.collection(u'Parks').document(doc.id).update({
        'votes':a+1,
        'rating':b+int(r)
    })
    now=session["uid"]
    doc = db.collection(u'Users').document(now).get()
    c=doc.to_dict()
    try:
        db.collection(u'Users').document(now).update({
            'parks':c['parks'].append(p),
        })
    
    except:
    
        db.collection(u'Users').document(now).update({
            'parks':[p],
        })
    
        
    
    return redirect(request.referrer)

@app.route('/info_items',methods=['GET', 'POST'])
def info_items():
    form=infoForm()
    #docs = db.collection(u'Comments').where(u'name', u'==', p).stream()
    dic=db.collection(u'Information').stream()
    docs = [{
      'id': 1,
      'name': 'name 1',
      'email': 'email 1'
    }, {
      'id': 2,
      'name': 'name 2',
      'email': 'email 2'
    }]
    print(form.email.data)
    if request.method == 'POST':
        print("hello")
        data = {
        "name": form.name.data,
        "job": form.job.data,
        "email": form.email.data
        }
        docs = db.collection(u'Information').stream()

        for doc in docs:
            dici = doc.to_dict()
            print(dici)
            if data["name"] == dici['name'] and data["job"] == dici['job'] and data["email"] == dici['email']:
                flash("עובד קיים")
                return
        db.collection(u'Information').document().set(data)
        print("hello2")
        return redirect(url_for('info_items'))

    arr=[]
    for doc in dic:
        d=doc.to_dict()
        d["id"] = doc.id
        print(d)

        arr.append(d)
    print("not")
    return render_template('info.html',admin=session["admin"],email=session["user"],info_items=arr,now=session["uid"],form=form)


@app.route('/info_items/<info_item_id>',methods=['GET'])
def delete_info_item(info_item_id):
    form=infoForm()
    db.collection(u'Information').document(info_item_id).delete()

    return redirect(url_for('info_items'))

@app.route('/comments/<post_id>/<text>/update',methods=['GET', 'POST'])
def update_comments(post_id,text):
    form=updateComment()
    if form.validate_on_submit():
        data={'text':form.comment.data}
        db.collection(u'Comments').document(post_id).update(data)
        return redirect(url_for('parks'))
    return render_template('updateComment.html',form=form,admin=session["admin"],text=text)

@app.route('/facilities', methods=['GET', 'POST'])
def facilities():
        form = facilitiesForm()
        if form.validate_on_submit():
            docs = db.collection(u'Parks').stream()
            parkData = {
                "name": form.parkNameDB.data,
                "parkFacility": request.form.getlist('facility')
            }
            canAddPark = False
            for doc in docs:
                dici = doc.to_dict()
                try:
                    if parkData['name'] == dici['name']:
                        canAddPark = True

                    if canAddPark:
                        # Deleting and creating a new park witch will be updated with the new facilities
                        db.collection(u'Parks').document(doc.id).delete()
                        db.collection(u'Parks').document().set(parkData)
                        flash("עדכן מתקנים")
                        break

                except Exception as err:
                    pass
            return redirect(url_for('facilities'))
        return render_template('facilities.html', data=data, admin=session["admin"], form=form)

def addData():
    # UP LOADING ALL PARKS TO FIRE-BASE
    for i in data:
        db.collection(u'Parks').document().set({"name": i['Name']})
        # db.collection(u'Parks').document().set({"name": i['Name'], "Other": i['other']})





@app.route('/Guests/<string:email>/update', methods=['GET', 'POST'])
def updateGuest(email):
    print("into UpdateGuest")
    docs = db.collection(u'Users').stream()
    canMakePark = True
    for doc in docs:
        dici = doc.to_dict()
        if  dici['email']==email :
            canMakePark = False
            rpost=dici['name']
            emailGuest=dici['email']
            wanted=dici
    if canMakePark:
        abort(403)
           
    else:
        rrpost=rpost
    ref_comment=db.collection(u'Users')
    ref_my=ref_comment.where(u'email',u'==',email).stream()
    for r in ref_my:
        rr=r.to_dict()['email']
        print(rr)

    form = PostForm()
    print(form.email.data)
    if form.validate_on_submit():
        print("after")
        guest_email = form.email.data
        guest_name = form.name.data
        guest_last = form.last.data
        guset_password=form.password.data
        print(guset_password)
        ref_comment=db.collection(u'Users')
        ref_my=ref_comment.where(u'email',u'==',email).get()
        field_updates={"name":guest_name,"last":guest_last,"email":guest_email}
        for r in ref_my:
            rr=ref_comment.document(r.id)
            rr.update(field_updates)
        
        flash('המשתמש התעדכן בהצלחה!', 'success')
        return redirect(url_for('AllGuest', email=emailGuest))
    elif request.method == 'GET':
        print("get")
        docs
        form.email.data = wanted['email']
        form.name.data = wanted['name']
        form.last.data=wanted['last']
        form.password=wanted['password']
    return render_template('CreateGuest.html', title='Update Guest',
                           form=form, legend='Update Guest')
 


@app.route('/Guests', methods=['GET', 'POST'])
def AllGuest():
    guets = db.collection(u'Users').stream()
    return render_template('AllUsers.html', guests=guets)


@app.route('/registerByAdmin',methods=['GET', 'POST'])
def registerByAdmin():
    form=signupForm()
    if request.method == 'POST':
        email=form.email.data
        password=form.password.data
        name=form.name.data
        last=form.last.data
        Admin=form.Admin.data
        user=auth.create_user_with_email_and_password(email,password)
        data={"name":name,"last":last,"email":email,"password":password,"admin":Admin}
        print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        info=auth.get_account_info(user['idToken'])['users'][0]['localId']
        db.collection(u'Users').document(info).set(data)
        return redirect(url_for("login"))

    return render_template('signup.html',form=form,us="Not Exist")

@app.route("/Guests/<string:email>")
def Option_guest(email):
    #post=db.collection(u'testComments').query.get_or_404(post_id)
    post=db.collection(u'Users').where(u'email',u'==',email).stream()

   # rpost=post.to_dict()['title']
    docs = db.collection(u'Users').stream()
    canMakePark = True
    #print(post_id)
    for doc in docs:
        dici = doc.to_dict()
        if  dici['email']==email :
            canMakePark = False
            rpost=dici['name']
            wanted=dici
    if canMakePark==True:
        flash("error!")
        rpost='name'
        wanted=dici
    else:
        rpost=wanted['email']

 
    print(post)
    #post = Post.query.get_or_404(post_id)
    return render_template('updateGuestOption.html', title=rpost, guest=wanted)



@app.route('/Guests/<string:email>/delete',methods=[ 'POST'])
def deleteGuest(email):
    ref_comment=db.collection(u'Users')
    ref_my=ref_comment.where(u'email',u'==',email).get()
    for r in ref_my:
        rr=ref_comment.document(r.id)
        rr.delete()
        firebase_admin.auth.delete_user(rr.id)

    flash('המשתמש נמחק!', 'success')
    return redirect(url_for('AllGuest'))




if __name__ == '__main__':
    app.run(debug=True)

