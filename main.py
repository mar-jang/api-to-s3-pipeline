import requests
import pandas as pd
import boto3
from io import StringIO
from botocore.exceptions import ClientError

# s3 bucket
API_URL = "https://jsonplaceholder.typicode.com/posts"
BUCKET_NAME = "mareeha-api-data-bucket"  
REGION = "us-east-1"
FILE_NAME = "api_data/posts_filtered.csv"

s3 = boto3.client("s3", region_name=REGION)

def ensure_bucket_exists(bucket_name):
    """Check if the bucket exists, otherwise create it."""
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f" Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            try:
                print(f" Bucket '{bucket_name}' not found. Creating it...")
                s3.create_bucket(Bucket=bucket_name)
                print(f" Bucket '{bucket_name}' created successfully.")
            except Exception as e:
                print(f" Failed to create bucket: {e}")
        else:
            print(f" Unexpected error checking bucket: {e}")

#Pull Data from API 
response = requests.get(API_URL)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Pulled {len(data)} records from API.")
else:
    raise Exception(f" API request failed with status code {response.status_code}")

# manipulate data
df = pd.DataFrame(data)
df["title_word_count"] = df["title"].apply(lambda x: len(x.split()))
filtered_df = df[df["title_word_count"] > 5]

print(f"✅ Filtered dataset to {len(filtered_df)} records.")

# Save as CSV in Memory 
csv_buffer = StringIO()
filtered_df.to_csv(csv_buffer, index=False)

# ensure bucket then upload
ensure_bucket_exists(BUCKET_NAME)

try:
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=FILE_NAME,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )
    print(f" File uploaded successfully to s3://{BUCKET_NAME}/{FILE_NAME}")
except Exception as e:
    print(f" Upload failed: {e}")
