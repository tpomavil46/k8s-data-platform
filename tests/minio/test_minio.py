import boto3
from datetime import datetime

# Get credentials from your config
MINIO_ROOT_USER = "admin"  # Replace with your actual user
MINIO_ROOT_PASSWORD = "YourPasswordHere"  # Replace with your actual password

# Configure S3 client for MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id=MINIO_ROOT_USER,
    aws_secret_access_key=MINIO_ROOT_PASSWORD,
    region_name='us-east-1'
)

# List buckets
print("Buckets in MinIO:")
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(f"  ✓ {bucket['Name']}")

# Write a test file
test_data = f"Test data written at {datetime.now()}"
s3.put_object(
    Bucket='hot-tier',
    Key='test/hello.txt',
    Body=test_data.encode('utf-8')
)
print("\n✓ Wrote test file to hot-tier/test/hello.txt")

# Read it back
response = s3.get_object(Bucket='hot-tier', Key='test/hello.txt')
content = response['Body'].read().decode('utf-8')
print(f"✓ Read back: {content}")

print("\n✓ MinIO is working!")
