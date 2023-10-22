from flask import Flask, render_template, request, jsonify,redirect,session,url_for
import json
from pymongo import MongoClient
import os
from functions import upload_profile_cover_to_aws
from functions import upload_gallery_to_aws

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
            uid=request.form.get('UserID')
            profile_image = request.files['ProfileImage']
            cover_image = request.files['CoverImage']
            gallery_1=request.files['GalleryImg1']
            gallery_2=request.files['GalleryImg2']
            gallery_3=request.files['GalleryImg3']
            gallery_4=request.files['GalleryImg4']
            gallery_5=request.files['GalleryImg5']
            profile_image.save("pf.jpg")
            cover_image.save("cover.jpg")
            gallery_1.save("G1.jpg")
            gallery_2.save("G2.jpg")
            gallery_3.save("G3.jpg")
            gallery_4.save("G4.jpg")
            gallery_5.save("G5.jpg")
            if request.files['ProfileImage'].filename != '':
                profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{uid}_profile_image.jpg')
                profile_image_url=profile_image_['url']
            elif request.files['ProfileImage'].filename == '':
                profile_image_url=request.form.get("UserProfileDefault")
                
            if request.files['CoverImage'].filename != '':
                CoverImage_=upload_profile_cover_to_aws('cover.jpg','bixid',f'{uid}_cover_image.jpg')
                CoverImage=CoverImage_['url']
            elif request.files['CoverImage'].filename == '':
                CoverImage=request.form.get("UserCoverDefault")
                
            if request.files['GalleryImg1'].filename != '':
                GalleryImg1_=upload_profile_cover_to_aws('G1.jpg','bixid',f'{uid}_g1.jpg')
                GalleryImg1=GalleryImg1_['url']
            elif request.files['GalleryImg1'].filename == '':
                GalleryImg1=request.form.get("DefaultGalleryImg1")
                
            if request.files['GalleryImg2'].filename != '':
                GalleryImg2_=upload_profile_cover_to_aws('G2.jpg','bixid',f'{uid}_g2.jpg')
                GalleryImg2=GalleryImg2_['url']
            elif request.files['GalleryImg2'].filename == '':
                GalleryImg2=request.form.get("DefaultGalleryImg2")
                
            if request.files['GalleryImg3'].filename != '':
                GalleryImg3_=upload_profile_cover_to_aws('G3.jpg','bixid',f'{uid}_g3.jpg')
                GalleryImg3=GalleryImg3_['url']
            elif request.files['GalleryImg3'].filename == '':
                GalleryImg3=request.form.get("DefaultGalleryImg3")
                
            if request.files['GalleryImg4'].filename != '':
                GalleryImg4_=upload_profile_cover_to_aws('G4.jpg','bixid',f'{uid}_g4.jpg')
                GalleryImg4=GalleryImg4_['url']
            elif request.files['GalleryImg4'].filename == '':
                GalleryImg4=request.form.get("DefaultGalleryImg4")
                
            if request.files['ProfileImage'].filename != '':
                GalleryImg5_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{uid}_g5.jpg')
                GalleryImg5=GalleryImg5_['url']
            elif request.files['GalleryImg5'].filename == '':
                GalleryImg5=request.form.get("DefaultGalleryImg5")
            
            print(uid)
            print('this is post request')
            userRecord={
                "UserID":uid,
                "FirstName":request.form.get("FName"),
                "LastName": request.form.get("LName"),
                "ProfileImage":profile_image_url,
                "CoverImage":CoverImage,
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
                    "IMG1":GalleryImg1,
                    "IMG2":GalleryImg2,
                    "IMG3":GalleryImg3,
                    "IMG4":GalleryImg4,
                    "IMG5":GalleryImg5,
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
            update_operation = {
            "$set": userRecord
        }

            filter_criteria = {"UserID": uid}
            collection.update_one(filter_criteria, update_operation)
            return  redirect(f"/{uid}")
        else:
            print(request.referrer)
            uid=request.referrer.split("/")[-1]
            users = collection.find({"UserID": uid})
            user=users[0]
            return render_template('update.html',user=user)
    except Exception as err:
            return str(err)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    # try:
        if request.method == 'POST':
            print(request.referrer)
            uid=request.referrer.split("/")[-1]
            profile_image = request.files['ProfileImage']
            cover_image = request.files['CoverImage']
            gallery_1=request.files['GalleryImg1']
            gallery_2=request.files['GalleryImg2']
            gallery_3=request.files['GalleryImg3']
            gallery_4=request.files['GalleryImg4']
            gallery_5=request.files['GalleryImg5']
            profile_image.save("pf.jpg")
            cover_image.save("cover.jpg")
            gallery_1.save("G1.jpg")
            gallery_2.save("G2.jpg")
            gallery_3.save("G3.jpg")
            gallery_4.save("G4.jpg")
            gallery_5.save("G5.jpg")
            if request.files['ProfileImage'].filename != '':
                profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{uid}_profile_image.jpg')
                profile_image_url=profile_image_['url']
            elif request.files['ProfileImage'].filename == '':
                profile_image_url=''
                
            if request.files['CoverImage'].filename != '':
                CoverImage_=upload_profile_cover_to_aws('cover.jpg','bixid',f'{uid}_cover_image.jpg')
                CoverImage=CoverImage_['url']
            elif request.files['CoverImage'].filename == '':
                CoverImage=''
                
            if request.files['GalleryImg1'].filename != '':
                GalleryImg1_=upload_profile_cover_to_aws('G1.jpg','bixid',f'{uid}_g1.jpg')
                GalleryImg1=GalleryImg1_['url']
            elif request.files['GalleryImg1'].filename == '':
                GalleryImg1=''
                
            if request.files['GalleryImg2'].filename != '':
                GalleryImg2_=upload_profile_cover_to_aws('G2.jpg','bixid',f'{uid}_g2.jpg')
                GalleryImg2=GalleryImg2_['url']
            elif request.files['GalleryImg2'].filename == '':
                GalleryImg2=''
                
            if request.files['GalleryImg3'].filename != '':
                GalleryImg3_=upload_profile_cover_to_aws('G3.jpg','bixid',f'{uid}_g3.jpg')
                GalleryImg3=GalleryImg3_['url']
            elif request.files['GalleryImg3'].filename == '':
                GalleryImg3=''
                
            if request.files['GalleryImg4'].filename != '':
                GalleryImg4_=upload_profile_cover_to_aws('G4.jpg','bixid',f'{uid}_g4.jpg')
                GalleryImg4=GalleryImg4_['url']
            elif request.files['GalleryImg4'].filename == '':
                GalleryImg4=''
                
            if request.files['ProfileImage'].filename != '':
                GalleryImg5_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{uid}_g5.jpg')
                GalleryImg5=GalleryImg5_['url']
            elif request.files['GalleryImg5'].filename == '':
                GalleryImg5=''
            
            uid=request.referrer.split("/")[-1]
            print('this is post request')
            userRecord={
                "UserID":uid,
                "FirstName":request.form.get("FName"),
                "LastName": request.form.get("LName"),
                "ProfileImage":profile_image_url,
                "CoverImage":CoverImage,
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
                    "IMG1":GalleryImg1,
                    "IMG2":GalleryImg2,
                    "IMG3":GalleryImg3,
                    "IMG4":GalleryImg4,
                    "IMG5":GalleryImg5,
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
         
            collection.insert_one(userRecord)
            print("done")
            return  redirect(f"/{uid}")
        else:
            return "non post"
    # except Exception as err:
    #     print
    #     return str(err)
    
@app.route("/gallery", methods=['GET', 'POST'])  
def gallery(): 
    try:
        uid=request.referrer.split("/")[-1]
        urlsss=request.url.split("/")
        urlsss[-1]=uid
        current_url ='/'.join(urlsss)
        print(request.referrer)
        users = collection.find({"UserID": uid})
        user=users[0] 
        return render_template("gallery.html",user=user,current_url=current_url)
    
    except Exception as err:
        return render_template("error.html")
    
    
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

  
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)


