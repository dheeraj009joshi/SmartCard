import boto3
from botocore.exceptions import NoCredentialsError
ACCESS_KEY='AKIA4C6C3STL37NFUWNO'
SECRET_KEY='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'
def upload_profile_cover_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return {"url":f"https://bixid.s3.amazonaws.com/{s3_file}"}
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
        return {"url":f"https://bixid.s3.amazonaws.com/{s3_file}"}
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# print(upload_gallery_to_aws("static/assets/paytm-176.png","smart-card-bixcube","this.jpg"))