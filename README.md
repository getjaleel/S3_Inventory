
# S3 Bucket Inventory Script

## Overview
This script generates an inventory of all objects in an Amazon S3 bucket, including:
- **Object Key**: Full path of the object in the bucket.
- **Size**: Size of the object in bytes.
- **Last Modified Date**: Timestamp of the last modification.
- **Key Parts**: Object keys containing underscores (`_`) are split into individual parts for analysis.

The output is stored in **CSV files**, and if the row limit of Excel (1,048,576 rows) is exceeded, the script automatically splits the data into multiple CSV files.

---

## Features
- **Bucket Validation**: Checks if the specified bucket exists in your AWS account.
- **Dynamic Key Parsing**: Splits object keys with underscores into individual parts.
- **Row Limit Handling**: Automatically creates additional CSV files if row limits are exceeded.
- **Progress Feedback**: Displays a spinner and object count during execution.
- **Summary**: Reports total objects processed and total files generated.

---

## Requirements

### Software Dependencies
1. **Python** (Version 3.6 or higher)
2. **AWS SDK for Python (Boto3)**: Install via pip:
   ``` pip install boto3```

AWS Setup
AWS credentials must be configured using the AWS CLI or environment variables:
```aws configure```
  Provide:
  
  Access Key ID
  Secret Access Key
  Default Region
  The AWS user must have the following permissions:
  
  s3:ListBucket
  s3:GetObject

## How to Run the Script
### Step 1: Download the Script
  Save the script file as s3_inventory_split.py in a working directory.

### Step 2: Open Terminal or Command Prompt
  Windows: Open Command Prompt (Win + R, then type cmd).
  macOS/Linux: Open a terminal.

### Step 3: Install Dependencies
  Run the following command to install the required Python package:
  pip install boto3

### Step 4: Run the Script
  python s3_inventory.py

### Step 5: Provide Bucket Name
  Enter the S3 bucket name for inventory: my-example-bucket

### Step 6: Check the Output

```The script will generate multiple CSV files in the current directory.
  s3_inventory_<bucket_name>_1.csv
  s3_inventory_<bucket_name>_2.csv
Fetching objects from bucket: my-example-bucket
Processing object 1048576 /
Row limit reached for s3_inventory_my-example-bucket_1.csv. Creating a new file...
Processing object 2097152 -
Row limit reached for s3_inventory_my-example-bucket_2.csv. Creating a new file...
Processing object 3000000 \

Total objects processed: 3000000
Total files generated: 3

Inventory report generated with split files: s3_inventory_my-example-bucket_*.csv
Total execution time: 320.65 seconds```
