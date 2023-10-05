from flask import Flask, render_template, request, jsonify,redirect
import json
from all_users import users

all_users = users
app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
  return "this is home"

@app.route('/<user_id>')
def index(user_id):
    user = None
    try:
      for i in all_users:
        if i['UserID'] == user_id:
          print(i['UserID'])
          user = i
      if user['Authentication']['Status_of_data'] == True:
        return render_template('index.html', user=user)
      else:
        return render_template('sign_up_form.html', user=user)
    except:
      return render_template('sign_up_form.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    print(request.referrer)
    uid=request.referrer.split("/")[-1]
    print('this is post request')
    userRecord={
        "UserID":uid,
        "FirstName":request.form.get("FName"),
        "LastName": request.form.get("LName"),
        "ProfileImage":request.form.get("ProfileImage"),
        "CoverImage":request.form.get("CoverImage"),
        "Contact": request.form.get("Contact"),
        "DOB":request.form.get("DOB"),
        "BusinessName": request.form.get("BusinessName"),
        "Designation":request.form.get("Designation"),
        "Website":request.form.get("Website"),
        "Socials": {
            "Twitter": request.form.get("Twitter"),
            "Instagram":request.form.get("Instagram"),
            "LinkedIn":request.form.get("LinkedIn"),
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
            "PhonePay":"",
            "Paytm":"",
            "BHIM":"",
        },
        
         
        "Authentication": {
            "Username": request.form.get("Email"),
            "Password": request.form.get("Password"),
            "Status_of_data": True,
        }
    }
    users.append(userRecord)
    f=open("all_users.py",'w',encoding='utf-8')
    f.write("users = "+str(users))
    f.close()
    return  redirect(f"/{uid}")
    
  
  else:
    return "non post"
  

app.run(debug=True)
