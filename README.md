S3 Bucket Inventory Script
Overview
The S3 Bucket Inventory Script generates a detailed inventory of all objects in an Amazon S3 bucket. It retrieves object metadata and outputs it into one or more CSV files. If the number of rows exceeds the Excel row limit (1,048,576 rows), the script automatically splits the data into multiple files.

Features
Validates the existence of the S3 bucket in the AWS account.
Dynamically handles object keys with varying structures and splits keys containing underscores (_) into individual parts.
Automatically splits data into multiple CSV files if row limits are exceeded.
Provides real-time progress updates during execution.
Outputs a summary of total objects processed and total files generated.
Requirements
Software Dependencies
Python (Version 3.6 or higher)
AWS SDK for Python (Boto3): Install via pip:
bash
Copy code
pip install boto3
CSV: Included in Python's standard library.
AWS Setup
AWS credentials must be configured using the AWS CLI, environment variables, or a configuration file:

bash
Copy code
aws configure
Provide:

Access Key ID
Secret Access Key
Default Region
The AWS user must have the following permissions:

s3:ListBucket
s3:GetObject
Usage
1. Download the Script
Save the script file as s3_inventory.py in your working directory.

2. Install Dependencies
Run the following command to install the required Python package:

bash
Copy code
pip install boto3
3. Run the Script
Execute the script in a terminal or command prompt:

bash
Copy code
python s3_inventory.py
4. Provide the Bucket Name
When prompted, enter the name of the S3 bucket:

mathematica
Copy code
Enter the S3 bucket name for inventory: my-example-bucket
5. Check the Output
The script generates one or more CSV files in the same directory as the script. If the row limit is exceeded, the files are split sequentially:

s3_inventory_<bucket_name>_1.csv
s3_inventory_<bucket_name>_2.csv
...
Example Output
For a bucket named ausseabed-mh370-cache-prod, the script might generate:

csharp
Copy code
Fetching objects from bucket: ausseabed-mh370-cache-prod
Processing object 1048576 /
Row limit reached for s3_inventory_ausseabed-mh370-cache-prod_1.csv. Creating a new file...
Processing object 2097152 -
Row limit reached for s3_inventory_ausseabed-mh370-cache-prod_2.csv. Creating a new file...
Processing object 3000000 \

Total objects processed: 3000000
Total files generated: 3

Inventory report generated with split files: s3_inventory_ausseabed-mh370-cache-prod_*.csv
Total execution time: 320.65 seconds
Notes
Row Limit Handling:

Each CSV file is limited to 1,048,576 rows to comply with Excel's row limit.
Additional files are created automatically when the limit is reached.
Progress Feedback:

The script displays real-time progress with a spinner and the current object count.
Error Handling:

If the bucket does not exist or there are permission issues, the script will display an appropriate error message and terminate.
Troubleshooting
Permission Issues
Ensure the AWS IAM user has s3:ListBucket and s3:GetObject permissions.
Verify credentials using:
bash
Copy code
aws sts get-caller-identity
File Splitting
If the script fails to generate multiple files, check disk space and ensure the file system supports large file writes.
Large Buckets
For buckets with millions of objects, ensure adequate disk space and consider running the script on a powerful machine.
