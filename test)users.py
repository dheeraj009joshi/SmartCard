from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority"
user_data={'UserID': 'Dheeraj', 'FirstName': 'dheeraj', 'LastName': 'joshi', 'ProfileImage': 'static/profile_cover_photos/Dheeraj.png', 'CoverImage': 'static/profile_cover_photos/animals-kali-linux-wallpaper-preview.jpg', 'Contact': '', 'DOB': '', 'BusinessName': 'dhanuinfo', 'Position': '', 'Designation': '', 'Website': '', 'Socials': {'Instagram': '', 'LinkedIn': '', 'Facebook': '', 'YouTube': '', 'GoogleMapUrl': '', 'SnapChat': '', 'DriveLink': ''}, 'About': {'GSTIN': None, 'PAN Number': '', 'AboutText': ''}, 'Location': {'Address': '123 Main Street, Cityville', 'ZipCode': '', 'Latitude': 134.563252, 'Longitude': 185.5342678}, 'Gallery': {'IMG1': 'static/gallery_photos/WhatsApp Image 2023-06-15 at 15.10.24.jpg', 'IMG2': 'static/gallery_photos/WhatsApp Image 2023-06-15 at 15.10.27.jpg', 'IMG3': 'static/gallery_photos/WhatsApp Image 2023-06-15 at 15.10.28.jpg', 'IMG4': 'static/gallery_photos/WhatsApp Image 2023-06-15 at 15.10.29.jpg', 'IMG5': 'static/gallery_photos/WhatsApp Image 2023-06-15 at 15.10.30.jpg'}, 'Payment': {'PayPal': 'johndoe_paypal@example.com', 'BankName': '', 'AccountHolderName': '', 'AccountNumber': '', 'IFSC': '', 'GooglePay': '', 'PhonePe': '07877424770', 'Paytm': '', 'UPI': ''}, 'Authentication': {'Username': 'dlovej009@gmail.com', 'Password': 'DHeeraj', 'Status_of_data': True}}
try:
   
    client = MongoClient(uri)
    db = client['myDb']
    collection = db['users']
    collection.insert_one(user_data)
    print("done")
except Exception as e:
    print(f'Error: {e}')

finally:
    if client:
        client.close()
        print('Connection closed')
