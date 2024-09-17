import requests
import boto3
from botocore.exceptions import NoCredentialsError

# Initialize the S3 client
s3_client = boto3.client('s3')

def download_and_upload_to_s3(url, bucket_name, s3_file_name):
    try:
        # Download the file from the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Upload the file directly to S3 from the downloaded stream
        s3_client.upload_fileobj(response.raw, bucket_name, s3_file_name)
        print(f"File uploaded to S3 bucket '{bucket_name}' with key '{s3_file_name}'")
    
    except requests.exceptions.RequestException as err:
        print(f"Error occurred while downloading the file: {err}")
    except NoCredentialsError:
        print("Credentials not available for AWS S3")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
url = "https://example.com/path-to-your-file"  # URL of the file to download
bucket_name = "your-s3-bucket-name"  # Name of your S3 bucket
s3_file_name = "folder/your-file-name.ext"  # The key (path) for the file in the S3 bucket

download_and_upload_to_s3(url, bucket_name, s3_file_name)
