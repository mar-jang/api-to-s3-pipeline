# API to S3 ETL Pipeline (Python + AWS)

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Python, Pandas, and AWS S3.  
It pulls data from a public REST API, performs basic transformations, and uploads the results to an Amazon S3 bucket.

Goal:  
Automatically fetch data from a REST API → transform it with Pandas → store it in a CSV file → upload it to an S3 bucket.

Data Source:  
[`https://jsonplaceholder.typicode.com/posts`]

Tools Used:

- Python 3.9+
- Pandas (data manipulation)
- Requests (API calls)
- Boto3 (AWS SDK for Python)
- StringIO (in-memory file buffer)

---

## How It Works

1. Extract the script sends a GET request to the public API to retrieve 100 posts.
2. Transform the data is loaded into a Pandas DataFrame, and a new column `title_word_count` is added.  
   (Only posts with more than 5 words in their title are kept.)
3. Load the filtered data is written to a CSV (in memory) and uploaded to your AWS S3 bucket.
