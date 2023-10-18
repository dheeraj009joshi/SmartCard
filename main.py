from flask import Flask, render_template, request, jsonify,redirect,session,url_for
import json
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='static')
uri = "mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['myDb']
collection = db['users']
app.secret_key = 'smart_card'

@app.route('/')
def home():
    
  return "this is home"

@app.route('/<user_id>')
def index(user_id):
    current_url = request.url
    user_list=list(collection.find({"UserID": user_id}))
    if user_list:
      if user_list[0]['Authentication']['Status_of_data'] == True:
            user_list[0].pop("_id",None)
            print(session)
            session['user']=user_list[0]
            try:
                if user_list[0]['Authentication']['Username'] == session['username']:
                    return render_template('index.html', user=user_list[0],login=True,current_url=current_url)
                else:   
                    return render_template('index.html', user=user_list[0],login=False,current_url=current_url)
            except:
                return render_template('index.html', user=user_list[0],login=False,current_url=current_url)
      else:
        return render_template('Update.html', user=user_list[0],current_url=current_url)
        
       
    else:
        return render_template('sign_up_form.html',user_id=user_id,current_url=current_url)
    
    
@app.route("/logout", methods=['GET', 'POST'])  
def logout(): 
    session.pop('username',None)
    session.pop('login',None)
    uid=request.referrer.split("/")[-1]
    return redirect(f"/{uid}")
@app.route("/login", methods=['GET', 'POST'])  
def login():
    try:
        print("this is login")
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # userS  =[]
            # for i in users:
            #     if i["Authentication"]["Username"]==username:
            #         userS.append(i)
            userS = list(collection.find({"Authentication.Username": username}))
            print(userS)
            if username in userS[0]['Authentication']['Username'] and userS[0]['Authentication']['Password'] == password:
                userS[0].pop("_id",None)
                session['username'] = username
                session['user']=userS[0]
                session['login']=True
                return redirect(f'/{userS[0]["UserID"]}')
            else:
                return  render_template('login.html', error="error")
        else:
            return render_template('login.html')
    except Exception as err:
        return render_template("error.html")
   
@app.route("/update", methods=['GET', 'POST']) 
def update_user():
    try:
        if request.method == 'POST':
            print(request.referrer)
            profile_image = request.files['ProfileImage']
            cover_image = request.files['CoverImage']
            gallery_1=request.files['GalleryImg1']
            gallery_2=request.files['GalleryImg2']
            gallery_3=request.files['GalleryImg3']
            gallery_4=request.files['GalleryImg4']
            gallery_5=request.files['GalleryImg5']
            try:
                # Save the uploaded files to a desired location
                profile_image.save(f'static/profile_cover_photos/{profile_image.filename}')
                cover_image.save(f'static/profile_cover_photos/{cover_image.filename}')
            except:
                pass
            try:
                gallery_1.save(f'static/gallery_photos/{gallery_1.filename}')
                gallery_2.save(f'static/gallery_photos/{gallery_2.filename}')
                gallery_3.save(f'static/gallery_photos/{gallery_3.filename}')
                gallery_4.save(f'static/gallery_photos/{gallery_4.filename}')
                gallery_5.save(f'static/gallery_photos/{gallery_5.filename}')
            except:
                pass
            uid=request.form.get('UserID')
            print(uid)
            print('this is post request')
            userRecord={
                "UserID":uid,
                "FirstName":request.form.get("FName"),
                "LastName": request.form.get("LName"),
                "ProfileImage":f"static/profile_cover_photos/{profile_image.filename}",
                "CoverImage":f"static/profile_cover_photos/{cover_image.filename}",
                "Contact": request.form.get("Contact"),
                "DOB":request.form.get("DOB"),
                "BusinessName": request.form.get("BusinessName"),
                "Position": request.form.get("Position"),
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
                
                },

                "Gallery": {
                    "IMG1":f"static/gallery_photos/{gallery_1.filename}",
                    "IMG2":f"static/gallery_photos/{gallery_2.filename}",
                    "IMG3":f"static/gallery_photos/{gallery_3.filename}",
                    "IMG4":f"static/gallery_photos/{gallery_4.filename}",
                    "IMG5":f"static/gallery_photos/{gallery_5.filename}",
                },
                "Payment": {
                    # "QRImage":"QRImage.jpg",
                    "PayPal": "johndoe_paypal@example.com",
                    # "CreditCard": "**** **** **** 1234",
                    "BankName":request.form.get("BankName"),
                    "AccountHolderName":request.form.get("AccountHolderName"),
                    "AccountNumber":request.form.get("AccountNumber"),
                    "IFSC":request.form.get("IFSC"),
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
            if userRecord['ProfileImage']=='static/profile_cover_photos/':
                userRecord['ProfileImage']=request.form.get("UserProfileDefault")
            if userRecord['CoverImage']=='static/profile_cover_photos/':
                userRecord['CoverImage']=request.form.get("UserCoverDefault")
            if userRecord['Gallery']['IMG1']=='static/gallery_photos/':
                userRecord['Gallery']['IMG1']=request.form.get("DefaultGalleryImg1")
            if userRecord['Gallery']['IMG2']=='static/gallery_photos/':
                userRecord['Gallery']['IMG2']=request.form.get("DefaultGalleryImg2")
            if userRecord['Gallery']['IMG3']=='static/gallery_photos/':
                userRecord['Gallery']['IMG3']=request.form.get("DefaultGalleryImg3")
            if userRecord['Gallery']['IMG4']=='static/gallery_photos/':
                userRecord['Gallery']['IMG4']=request.form.get("DefaultGalleryImg4")
            if userRecord['Gallery']['IMG5']=='static/gallery_photos/':
                userRecord['Gallery']['IMG5']=request.form.get("DefaultGalleryImg5")
        
            update_operation = {
            "$set": userRecord
        }
            # user =None
            # index=0
            # for i in users:
            #     if i["UserID"]==uid:
            #         user=i
            #         break
            #     index+=1 
            # users[index]= userRecord 
            # f=open("all_users.py",'w',encoding='utf-8')
            # f.write("users = "+str(users))
            # f.close() 
            # # # # # # set user = userdetails
            filter_criteria = {"UserID": uid}
            collection.update_one(filter_criteria, update_operation)
            return  redirect(f"/{uid}")
        else:
            print(request.referrer)
            uid=request.referrer.split("/")[-1]
            user_list  =[]
            for i in users:
                if i["UserID"]==uid:
                    user_list.append(i)
            users = collection.find({"UserID": uid})
            user=users[0]
            return render_template('update.html',user=user)
    except Exception as err:
            return render_template('error.html')   
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        from all_users import users
        if request.method == 'POST':
            print(request.referrer)
            profile_image = request.files['ProfileImage']
            cover_image = request.files['CoverImage']
            gallery_1=request.files['GalleryImg1']
            gallery_2=request.files['GalleryImg2']
            gallery_3=request.files['GalleryImg3']
            gallery_4=request.files['GalleryImg4']
            gallery_5=request.files['GalleryImg5']
            try:
                # Save the uploaded files to a desired location
                profile_image.save(f'static/profile_cover_photos/{profile_image.filename}')
                cover_image.save(f'static/profile_cover_photos/{cover_image.filename}')
            except:
                pass
            try:
                gallery_1.save(f'static/gallery_photos/{gallery_1.filename}')
                gallery_2.save(f'static/gallery_photos/{gallery_2.filename}')
                gallery_3.save(f'static/gallery_photos/{gallery_3.filename}')
                gallery_4.save(f'static/gallery_photos/{gallery_4.filename}')
                gallery_5.save(f'static/gallery_photos/ {gallery_5.filename}')
            except:
                pass
            uid=request.referrer.split("/")[-1]
            print('this is post request')
            userRecord={
                "UserID":uid,
                "FirstName":request.form.get("FName"),
                "LastName": request.form.get("LName"),
                "ProfileImage":f"static/profile_cover_photos/{profile_image.filename}",
                "CoverImage":f"static/profile_cover_photos/{cover_image.filename}",
                "Contact": request.form.get("Contact"),
                "DOB":request.form.get("DOB"),
                "BusinessName": request.form.get("BusinessName"),
                "Position": request.form.get("Position"),
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
                
                },

                "Gallery": {
                    "IMG1":f"static/gallery_photos/{gallery_1.filename}",
                    "IMG2":f"static/gallery_photos/{gallery_2.filename}",
                    "IMG3":f"static/gallery_photos/{gallery_3.filename}",
                    "IMG4":f"static/gallery_photos/{gallery_4.filename}",
                    "IMG5":f"static/gallery_photos/{gallery_5.filename}",
                },
                "Payment": {
                    # "QRImage":"QRImage.jpg",
                    "PayPal": request.form.get("paypal"),
                    # "CreditCard": "**** **** **** 1234",
                    "BankName":request.form.get("BankName"),
                    "AccountHolderName":request.form.get("AccountHolderName"),
                    "AccountNumber":request.form.get("AccountNumber"),
                    "IFSC":request.form.get("IFSC"),
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
            # users.append(userRecord)
            # users.append(userRecord)
            collection.insert_one(userRecord)
            print("done")
            return  redirect(f"/{uid}")
        else:
            return "non post"
    except Exception as err:
        return render_template("error.html")
    
@app.route("/gallery", methods=['GET', 'POST'])  
def gallery(): 
    try:
        uid=request.referrer.split("/")[-1]
        urlsss=request.url.split("/")
        urlsss[-1]=uid
        current_url ='/'.join(urlsss)
        print(request.referrer)
        user_list  =[]
        for i in users:
            if i["UserID"]==uid:
                user_list.append(i)
        users = collection.users.find({"UserID": uid})
        user=user_list[0] 
        return render_template("gallery.html",user=user,current_url=current_url)
    
    except Exception as err:
        return render_template("error.html")
    
    
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

  
port = int(os.environ.get('PORT', 5000))
app.run(debug=True, host='0.0.0.0',port=port)
