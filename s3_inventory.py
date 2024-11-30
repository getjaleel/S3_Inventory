import boto3
import csv
import os
import sys
import time
import itertools

ROW_LIMIT = 1_048_576  # Excel's maximum row limit

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Displays the script banner and details."""
    banner = """
    ###########################################################
    #                S3 Bucket Inventory Script              #
    ###########################################################
    - This script generates an inventory of all objects in an S3 bucket.
    - The output is stored in CSV files in the current directory.
    - Automatically splits data into multiple files if row limit is exceeded.
    """
    print(banner)

def check_bucket_exists(bucket_name):
    """Check if the S3 bucket exists in the account."""
    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name in bucket_names:
            print(f"Bucket '{bucket_name}' has been found in your account. Proceeding...\n")
            return True
        else:
            print(f"Bucket '{bucket_name}' does not exist in your account.\n")
            return False
    except Exception as e:
        print(f"An error occurred while checking the bucket: {e}")
        sys.exit(1)

def fetch_and_write_objects(bucket_name, base_file_name):
    """Fetch objects and write incrementally to multiple CSV files."""
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    print(f"Fetching objects from bucket: {bucket_name}")

    base_fieldnames = ['Original Key', 'Size (Bytes)', 'LastModified']
    dynamic_fieldnames = set()  # To track additional parts dynamically
    total_objects = 0  # To track the total number of objects
    spinner = itertools.cycle(["|", "/", "-", "\\"])  # Spinner for visual feedback
    current_file_index = 1  # Index to track file splits
    current_row_count = 0  # Track rows in the current file

    # Initialize CSV file
    current_file_name = f"{base_file_name}_{current_file_index}.csv"
    csvfile = open(current_file_name, 'w', newline='')
    writer = None

    try:
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get('Contents', []):
                # Parse object key
                key_parts = obj['Key'].split('_') if '_' in obj['Key'] else [obj['Key']]
                new_fieldnames = {f"Part_{i+1}" for i in range(len(key_parts))}
                dynamic_fieldnames.update(new_fieldnames)

                # Update fieldnames and writer if necessary
                if writer is None or any(field not in writer.fieldnames for field in dynamic_fieldnames):
                    all_fieldnames = base_fieldnames + sorted(dynamic_fieldnames)
                    writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
                    if current_row_count == 0:  # Only write header once per file
                        writer.writeheader()

                # Create the record
                record = {
                    "Original Key": obj['Key'],
                    "Size (Bytes)": obj['Size'],
                    "LastModified": obj['LastModified'].isoformat(),
                    **{f"Part_{i+1}": part for i, part in enumerate(key_parts)}
                }
                writer.writerow(record)
                total_objects += 1
                current_row_count += 1

                # Display progression
                print(f"\rProcessing object {total_objects} {next(spinner)}", end="")

                # Check if row limit is exceeded
                if current_row_count >= ROW_LIMIT:
                    print(f"\nRow limit reached for {current_file_name}. Creating a new file...")
                    csvfile.close()
                    current_file_index += 1
                    current_file_name = f"{base_file_name}_{current_file_index}.csv"
                    csvfile = open(current_file_name, 'w', newline='')
                    writer = None  # Reset writer
                    current_row_count = 0  # Reset row count for new file

    finally:
        csvfile.close()  # Ensure the file is closed

    print()  # Move to the next line after processing
    print(f"Total objects processed: {total_objects}")
    print(f"Total files generated: {current_file_index}")

def generate_bucket_inventory():
    """Main function to prompt for bucket name, validate, and generate CSV."""
    clear_screen()
    display_banner()
    bucket_name = input("Enter the S3 bucket name for inventory: ").strip()

    # Timer starts
    start_time = time.time()

    # Check if bucket exists
    if not check_bucket_exists(bucket_name):
        print("Please check the bucket name and try again.\n")
        sys.exit(1)

    # File name base
    base_file_name = f"s3_inventory_{bucket_name}"

    # Fetch and write objects incrementally
    fetch_and_write_objects(bucket_name, base_file_name)

    # Timer ends
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nInventory report generated with split files: {base_file_name}_*.csv")
    print(f"Total execution time: {elapsed_time:.2f} seconds")

# Run the script
if __name__ == "__main__":
    generate_bucket_inventory()

