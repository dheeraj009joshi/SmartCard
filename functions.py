import boto3
from botocore.exceptions import NoCredentialsError
ACCESS_KEY='AKIAQ2OXKKWK52QARBV4'
SECRET_KEY='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'
def upload_profile_cover_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return {"url":f"s3://smart-card-bixcube/Profile_cover_images/{s3_file}"}
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
    
    
def upload_gallery_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return {"url":f"https://smart-card-bixcube.s3.amazonaws.com/{s3_file}"}
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

print(upload_gallery_to_aws("static/assets/paytm-176.png","smart-card-bixcube","this.jpg"))