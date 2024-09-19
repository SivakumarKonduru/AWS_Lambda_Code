import boto3
import time

# Initialize the boto3 client
ec2_client = boto3.client('ec2')

def import_ova_to_ami(s3_bucket_name, s3_ova_key, ami_name, instance_type="m5.large"):
    try:
        # Step 1: Import OVA as an image
        response = ec2_client.import_image(
            Description=f"Import of {ami_name} from OVA",
            DiskContainers=[
                {
                    'Description': 'OVA Import',
                    'Format': 'ova',
                    'UserBucket': {
                        'S3Bucket': s3_bucket_name,
                        'S3Key': s3_ova_key
                    }
                }
            ]
        )
        
        import_task_id = response['ImportTaskId']
        print(f"Import task started with task ID: {import_task_id}")
        
        # Step 2: Wait for the import process to complete
        while True:
            task_status = ec2_client.describe_import_image_tasks(ImportTaskIds=[import_task_id])
            status = task_status['ImportImageTasks'][0]['Status']
            print(f"Current status: {status}")
            
            if status == 'completed':
                image_id = task_status['ImportImageTasks'][0]['ImageId']
                print(f"Import completed successfully. Image ID: {image_id}")
                return image_id
            elif status == 'deleted' or status == 'deleted':
                print("The import task failed.")
                return None
            
            # Wait before checking the status again
            time.sleep(30)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
s3_bucket_name = "your-s3-bucket-name"  # Replace with your S3 bucket name
s3_ova_key = "path-to-your-ova-file.ova"  # Replace with the OVA file path in S3
ami_name = "your-ami-name"  # Replace with a desired AMI name

# Call the function to import the OVA and create an AMI
ami_id = import_ova_to_ami(s3_bucket_name, s3_ova_key, ami_name)

if ami_id:
    print(f"AMI created successfully: {ami_id}")
else:
    print("Failed to import OVA and create AMI.")
