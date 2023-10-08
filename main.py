from flask import Flask, render_template, request, jsonify,redirect,session,url_for
import json
from pymongo import MongoClient
# from flask_pymongo import PyMongo

app = Flask(__name__, static_folder='static')
# app.config["MONGO_URI"] = "mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority/myDb"
url="mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority"

cluster=MongoClient(url)
db=cluster['myDb']
collection=db['users']
app.secret_key = 'smart_card'
# mongo = PyMongo(app)
# from all_users import users
users = list(collection.users.find({}))
all_users = users
print(all_users)

@app.route('/')
def home():
    
  return "this is home"

@app.route('/<user_id>')
def index(user_id):
    user = None
    users = collection.users.find({"UserID": user_id})
    user_list = list(users)
    if user_list:
      if user_list[0]['Authentication']['Status_of_data'] == True:
            user_list[0].pop("_id",None)
            print(session)
            session['user']=user_list[0]
            try:
                if user_list[0]['Authentication']['Username'] == session['username']:
                    return render_template('index.html', user=user_list[0],login=True)
                else:   
                    return render_template('index.html', user=user_list[0],login=False)
            except:
                return render_template('index.html', user=user_list[0],login=False)
      else:
        return render_template('Update.html', user=user_list[0])
        
       
    else:
        return "404 not valid card"
        # # No users found for the given email
        # return render_template('sign_up_form.html')
    
    
@app.route("/logout", methods=['GET', 'POST'])  
def logout(): 
    session.pop('username',None)
    session.pop('login',None)
    uid=request.referrer.split("/")[-1]
    return redirect(f"/{uid}")
@app.route("/login", methods=['GET', 'POST'])  
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = list(collection.users.find({"Authentication.Username": username}))
        print(users)
        if username in users[0]['Authentication']['Username'] and users[0]['Authentication']['Password'] == password:
            users[0].pop("_id",None)
            session['username'] = username
            session['user']=users[0]
            session['login']=True
            return redirect(f'/{users[0]["UserID"]}')
        else:
            return  render_template('login.html', error="error")
    else:
        return render_template('login.html')
   
@app.route("/update", methods=['GET', 'POST']) 
def update_user():
    if request.method == 'POST':
        print(request.referrer)
        profile_image = request.files['ProfileImage']
        cover_image = request.files['CoverImage']
        try:
            # Save the uploaded files to a desired location
            profile_image.save(f'static/{profile_image.filename}')
            cover_image.save(f'static/{cover_image.filename}')
        except:
            pass
        
        uid=request.form.get('UserID')
        print(uid)
        print('this is post request')
        userRecord={
            "UserID":uid,
            "FirstName":request.form.get("FName"),
            "LastName": request.form.get("LName"),
            "ProfileImage":f"static/{profile_image.filename}",
            "CoverImage":f"static/{cover_image.filename}",
            "Contact": request.form.get("Contact"),
            "DOB":request.form.get("DOB"),
            "BusinessName": request.form.get("BusinessName"),
            "Designation":request.form.get("Designation"),
            "Website":request.form.get("Website"),
            "Socials": {
                "Instagram":request.form.get("Instagram"),
                "LinkedIn":request.form.get("LinkedIn"),
                "Facebook":request.form.get("Facebook"),
                "YouTube":request.form.get("YouTube"),
                "GoogleMapUrl":request.form.get("GoogleMapUrl"),
                "SnapChat":request.form.get("SnapChat"),
                "DriveLink":request.form.get("DriveLink")
            },
            "About":{
                "GSTIN":request.form.get("GSTIN"),
                "PAN Number":"",
                "AboutText":request.form.get("aboutText")
            },
            "Location": {
                "Address": "123 Main Street, Cityville",
                "ZipCode":"",
                "Latitude": 134.563252,
                "Longitude": 185.5342678,
                "MapUrl": "https://map.google.com/xyz…"
            },

            "Gallery": {
                "IMG1":"",
                "IMG2":"",
                "IMG3":"",
                "IMG4":"",
                "IMG5":"",
            },
            "Payment": {
                "QRImage":"QRImage.jpg",
                "PayPal": "johndoe_paypal@example.com",
                "CreditCard": "**** **** **** 1234",
                "BankName":"",
                "AccountHolderName":"",
                "AccountNumber":"",
                "IFSC":"",
                "GooglePay":request.form.get("GooglePay"),
                "PhonePe":request.form.get("PhonePe"),
                "Paytm":request.form.get("Paytm"),
                "UPI":request.form.get("UPI"),
            },
            
            
            "Authentication": {
                "Username": request.form.get("Email"),
                "Password": request.form.get("Password"),
                "Status_of_data": True,
            }
        }
       
        update_operation = {
        "$set": userRecord
    }
        filter_criteria = {"UserID": uid}
        collection.users.update_one(filter_criteria, update_operation)
        return  redirect(f"/{uid}")
    else:
        print(request.referrer)
        uid=request.referrer.split("/")[-1]
        users = collection.users.find({"UserID": uid})
        user=(list(users))[0]
        return render_template('update.html',user=user)
        
    
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    print(request.referrer)
    profile_image = request.files['ProfileImage']
    cover_image = request.files['CoverImage']
    try:
        # Save the uploaded files to a desired location
        profile_image.save(f'static/{profile_image.filename}')
        cover_image.save(f'static/{cover_image.filename}')
    except:
        pass
    
    uid=request.referrer.split("/")[-1]
    print('this is post request')
    userRecord={
        "UserID":uid,
        "FirstName":request.form.get("FName"),
        "LastName": request.form.get("LName"),
        "ProfileImage":f"static/{profile_image.filename}",
        "CoverImage":f"static/{cover_image.filename}",
        "Contact": request.form.get("Contact"),
        "DOB":request.form.get("DOB"),
        "BusinessName": request.form.get("BusinessName"),
        "Designation":request.form.get("Designation"),
        "Website":request.form.get("Website"),
        "Socials": {
            "Twitter": request.form.get("Twitter"),
            "Instagram":request.form.get("Instagram"),
            "LinkedIn":request.form.get("LinkedIn"),
            "Facebook":request.form.get("Facebook"),
            "YouTube":request.form.get("YouTube"),
            "GoogleMapUrl":request.form.get("GoogleMapUrl"),
            "SnapChat":request.form.get("SnapChat"),
            "DriveLink":request.form.get("DriveLink")
        },
        "About":{
            "GSTIN":"",
            "PAN Number":"",
            "AboutText":request.form.get("aboutText")
        },
        "Location": {
            "Address": "123 Main Street, Cityville",
            "ZipCode":"",
            "Latitude": 134.563252,
            "Longitude": 185.5342678,
            "MapUrl": "https://map.google.com/xyz…"
        },

        "Gallery": {
            "IMG1":"",
            "IMG2":"",
            "IMG3":"",
            "IMG4":"",
            "IMG5":"",
        },
        "Payment": {
            "QRImage":"QRImage.jpg",
            "PayPal": "johndoe_paypal@example.com",
            "CreditCard": "**** **** **** 1234",
            "BankName":"",
            "AccountHolderName":"",
            "AccountNumber":"",
            "IFSC":"",
            "GooglePay":"",
            "PhonePe":"",
            "Paytm":"",
            "UPI":"",
        },
        
         
        "Authentication": {
            "Username": request.form.get("Email"),
            "Password": request.form.get("Password"),
            "Status_of_data": True,
        }
    }
    # users.append(userRecord)

    collection.users.insert_one(userRecord)
    f=open("all_users.py",'w',encoding='utf-8')
    f.write("users = "+str(users))
    f.close()
    return  redirect(f"/{uid}")
    
  
  else:
    return "non post"
  

app.run(debug=True)
